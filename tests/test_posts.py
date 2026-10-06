import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Thread

from bs4 import BeautifulSoup
import pytest
import requests
from werkzeug.serving import make_server


def page(response):
    return BeautifulSoup(response.get_data(as_text=True), "html.parser")


def add_post(client, title="테스트 제목", body="첫 줄\n둘째 줄"):
    response = client.post("/board/new", data={"title": title, "body": body})
    assert response.status_code == 303
    return int(response.headers["Location"].rsplit("/", 1)[1])


def test_empty_list_and_blank_form(client, rows):
    response = client.get("/")
    assert response.status_code == 200
    assert "등록된 게시글이 없습니다." in response.get_data(as_text=True)
    assert page(response).find("a", string=lambda text: text and "새 글 작성" in text)
    form = page(client.get("/board/new"))
    assert form.select_one("#title")["value"] == ""
    assert form.select_one("#body").text == ""
    assert rows() == []


def test_create_trim_redirect_detail_refresh_and_list_links(client, rows):
    first_id = add_post(client, "  새 이야기 \t", " \n 첫 줄\n둘째 줄  ")
    assert rows() == [(first_id, "새 이야기", "첫 줄\n둘째 줄")]
    for _ in range(3):
        detail = client.get(f"/board/{first_id}")
        assert detail.status_code == 200
        html = page(detail)
        assert html.select_one(".post-body").text == "첫 줄\n둘째 줄"
        assert "새 이야기" in html.h1.text
        assert f"게시글 번호 {first_id}" in html.text
        links = {anchor.get("href") for anchor in html.select("a")}
        assert {"/", f"/board/{first_id}/edit", f"/board/{first_id}/delete"}.issubset(links)
    assert len(rows()) == 1
    second_id = add_post(client, "두 번째 글", "두 번째 내용")
    listing = page(client.get("/"))
    assert [int(cell.text) for cell in listing.select(".post-number")] == [first_id, second_id]
    assert [link["href"] for link in listing.select(".post-link")] == [f"/board/{first_id}", f"/board/{second_id}"]


@pytest.mark.parametrize("values", [
    {"title": "", "body": "남겨둘 내용"},
    {"title": " \n\t", "body": "남겨둘 내용"},
    {"title": "남겨둘 제목", "body": ""},
    {"title": "남겨둘 제목", "body": " \n\t"},
    {},
])
def test_invalid_create_returns_400_and_preserves_input(client, rows, values):
    response = client.post("/board/new", data=values)
    assert response.status_code == 400
    assert rows() == []
    html = page(response)
    assert html.select_one("#title")["value"] == values.get("title", "")
    assert html.select_one("#body").text == values.get("body", "")
    assert html.select_one('[role="alert"]') is not None


def test_edit_get_is_read_only_and_populates_values(client, rows):
    post_id = add_post(client)
    before = rows()
    response = client.get(f"/board/{post_id}/edit")
    assert response.status_code == 200
    form = page(response)
    assert form.select_one("#title")["value"] == "테스트 제목"
    assert form.select_one("#body").text == "첫 줄\n둘째 줄"
    assert rows() == before


def test_edit_updates_only_selected_row_and_redirects_303(client, rows):
    first_id = add_post(client)
    second_id = add_post(client, "유지할 제목", "유지할 내용")
    response = client.post(f"/board/{first_id}/edit", data={"title": "  바뀐 제목 ", "body": " 바뀐 내용\n "})
    assert response.status_code == 303
    assert response.headers["Location"] == f"/board/{first_id}"
    assert rows() == [(first_id, "바뀐 제목", "바뀐 내용"), (second_id, "유지할 제목", "유지할 내용")]
    assert "바뀐 제목" in client.get("/").get_data(as_text=True)
    detail = client.get(response.headers["Location"]).get_data(as_text=True)
    assert "바뀐 제목" in detail and "바뀐 내용" in detail


@pytest.mark.parametrize("values", [
    {"title": "", "body": "시도한 내용"},
    {"title": " \t\n", "body": "시도한 내용"},
    {"title": "시도한 제목", "body": ""},
    {"title": "시도한 제목", "body": "  \n\t"},
    {},
])
def test_invalid_edit_keeps_original_database_and_redisplays_attempt(client, rows, values):
    post_id = add_post(client)
    before = rows()
    response = client.post(f"/board/{post_id}/edit", data=values)
    assert response.status_code == 400
    assert rows() == before
    html = page(response)
    assert html.select_one("#title")["value"] == values.get("title", "")
    assert html.select_one("#body").text == values.get("body", "")


def test_delete_confirmation_cancel_and_delete_only_target(client, rows):
    post_id = add_post(client)
    keep_id = add_post(client, "보존할 글", "삭제하지 않을 내용")
    before = rows()
    confirmation = client.get(f"/board/{post_id}/delete")
    assert confirmation.status_code == 200
    html = page(confirmation)
    assert "테스트 제목" in html.select_one(".delete-preview").text
    assert html.find("button", string="삭제 확인") is not None
    cancel = html.find("a", string="취소")
    assert cancel["href"] == f"/board/{post_id}"
    assert client.get(cancel["href"]).status_code == 200
    assert rows() == before
    response = client.post(f"/board/{post_id}/delete")
    assert response.status_code == 303 and response.headers["Location"] == "/"
    assert rows() == [(keep_id, "보존할 글", "삭제하지 않을 내용")]
    assert "테스트 제목" not in client.get("/").get_data(as_text=True)
    for suffix in ("", "/edit", "/delete"):
        assert client.get(f"/board/{post_id}{suffix}").status_code == 404
    assert client.post(f"/board/{post_id}/edit", data={"title": "없음", "body": "없음"}).status_code == 404
    assert client.post(f"/board/{post_id}/delete").status_code == 404
    assert add_post(client, "새 글", "새 내용") > keep_id


@pytest.mark.parametrize("method,suffix", [
    ("GET", ""), ("GET", "/edit"), ("GET", "/delete"),
    ("POST", "/edit"), ("POST", "/delete"),
])
def test_missing_posts_use_error_template_and_404(client, rows, method, suffix):
    response = client.open(f"/board/999999{suffix}", method=method)
    assert response.status_code == 404
    assert "게시글을 찾을 수 없습니다." in response.get_data(as_text=True)
    assert page(response).select_one(".error-code").text == "404"
    assert rows() == []


def test_html_and_sql_metacharacters_remain_text(client, rows):
    title = "O'Reilly'); DROP TABLE posts; -- <script>alert(1)</script>"
    body = "<img src=x onerror=alert(1)> & 'quote'\n다음 줄"
    post_id = add_post(client, title, body)
    assert rows() == [(post_id, title, body)]
    detail = page(client.get(f"/board/{post_id}"))
    assert detail.h1.text == title
    assert detail.select_one(".post-body").text == body
    assert detail.find("script") is None and detail.find("img") is None


def test_unknown_url_returns_error_template(client):
    response = client.get("/not-found")
    assert response.status_code == 404
    assert page(response).select_one(".error-code").text == "404"


def test_actual_monitor_collects_board_requests_without_form_data(application, client, tmp_path):
    monitor_source = Path(__file__).resolve().parents[1] / "mini-watch" / "monitor" / "backend" / "app.py"
    spec = importlib.util.spec_from_file_location("sample_monitor", monitor_source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monitor = module.create_app(tmp_path / "monitor.jsonl")
    server = make_server("127.0.0.1", 0, monitor)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    endpoint = f"http://127.0.0.1:{server.server_port}/logs"
    application.config["MONITOR_URL"] = endpoint
    try:
        assert client.get("/").status_code == 200
        assert client.post("/board/new?secret=never-log", data={"title": "private-title", "body": "private-body"}).status_code == 303
        assert client.post("/board/new", data={"title": " ", "body": "private-body"}).status_code == 400
        assert client.get("/board/999999").status_code == 404
        collected = requests.get(endpoint, timeout=2).json()
        assert [entry["status_code"] for entry in collected] == [200, 303, 400, 404]
        assert [entry["path"] for entry in collected] == ["/", "/board/new", "/board/new", "/board/999999"]
        local = Path(application.config["REQUEST_LOG_PATH"]).read_text(encoding="utf-8")
        assert len(local.splitlines()) == 4
        serialized = json.dumps(collected) + local
        assert all(secret not in serialized for secret in ["never-log", "private-title", "private-body"])
    finally:
        server.shutdown()
        worker.join(timeout=3)
        server.server_close()


def test_monitor_unavailable_does_not_block_crud(application, client, monkeypatch):
    def unavailable(*args, **kwargs):
        raise requests.ConnectionError("receiver offline")
    monkeypatch.setattr("request_logging.requests.post", unavailable)
    application.config["MONITOR_URL"] = "http://127.0.0.1:1/logs"
    assert client.get("/").status_code == 200
    assert client.post("/board/new", data={"title": "제목", "body": "내용"}).status_code == 303


def test_committed_post_is_readable_in_a_new_application_process(application, client, tmp_path):
    post_id = add_post(client, "재시작 후에도 남는 글", "PostgreSQL에 영구 저장된 내용")
    environment = os.environ.copy()
    environment["POSTS_TEST_DATABASE_URL"] = application.config["DATABASE_URL"]
    environment["POSTS_TEST_LOG_PATH"] = str(tmp_path / "new-process.log")
    environment["POSTS_TEST_POST_ID"] = str(post_id)
    code = """
import os
from app import create_app
app = create_app({
    'TESTING': True,
    'DATABASE_URL': os.environ['POSTS_TEST_DATABASE_URL'],
    'MONITOR_URL': '',
    'REQUEST_LOG_PATH': os.environ['POSTS_TEST_LOG_PATH'],
})
response = app.test_client().get('/board/' + os.environ['POSTS_TEST_POST_ID'])
assert response.status_code == 200
assert '재시작 후에도 남는 글' in response.get_data(as_text=True)
assert 'PostgreSQL에 영구 저장된 내용' in response.get_data(as_text=True)
"""
    general = Path(__file__).resolve().parents[1] / "mini-watch" / "general"
    subprocess.run(
        [sys.executable, "-c", code], cwd=general, env=environment,
        check=True, capture_output=True, timeout=20,
    )
