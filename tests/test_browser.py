from pathlib import Path
from threading import Thread

from playwright.sync_api import expect, sync_playwright
import pytest
from werkzeug.serving import make_server


@pytest.mark.browser
@pytest.mark.parametrize("width,height,name", [(1280, 900, "desktop"), (390, 844, "mobile")])
def test_connected_crud_flow_in_browser(application, rows, width, height, name):
    server = make_server("127.0.0.1", 0, application, threaded=True)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f"http://127.0.0.1:{server.server_port}"
    screenshots = Path(__file__).resolve().parents[1] / ".cache" / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            screen = browser.new_page(viewport={"width": width, "height": height})
            screen.goto(base)
            expect(screen.get_by_text("등록된 게시글이 없습니다.")).to_be_visible()
            screen.get_by_role("link", name="새 글 작성", exact=False).first.click()
            screen.get_by_label("제목").fill("나의 첫 번째 이야기")
            screen.get_by_label("내용").fill("일상 속 작은 생각을 남겨봅니다.\n함께 나누는 이야기가 모여 새로운 영감이 됩니다.")
            screen.get_by_role("button", name="게시글 저장").click()
            expect(screen.get_by_role("heading", name="나의 첫 번째 이야기")).to_be_visible()
            screen.reload()
            assert len(rows()) == 1
            screen.get_by_role("link", name="목록으로", exact=False).click()
            expect(screen.get_by_role("link", name="나의 첫 번째 이야기")).to_be_visible()
            assert screen.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            screen.screenshot(path=str(screenshots / f"board-{name}.png"), full_page=True)
            screen.get_by_role("link", name="나의 첫 번째 이야기").click()
            screen.get_by_role("link", name="수정하기").click()
            expect(screen.get_by_label("제목")).to_have_value("나의 첫 번째 이야기")
            screen.get_by_label("제목").fill("   ")
            response = None
            with screen.expect_response(lambda item: item.url.endswith("/edit") and item.request.method == "POST") as response:
                screen.get_by_role("button", name="수정 저장").click()
            assert response.value.status == 400
            assert rows()[0][1] == "나의 첫 번째 이야기"
            screen.get_by_label("제목").fill("조금 더 다듬은 이야기")
            screen.get_by_role("button", name="수정 저장").click()
            expect(screen.get_by_role("heading", name="조금 더 다듬은 이야기")).to_be_visible()
            screen.get_by_role("link", name="삭제하기").click()
            screen.get_by_role("link", name="취소", exact=True).click()
            expect(screen.get_by_role("heading", name="조금 더 다듬은 이야기")).to_be_visible()
            assert len(rows()) == 1
            screen.get_by_role("link", name="삭제하기").click()
            screen.get_by_role("button", name="삭제 확인").click()
            expect(screen.get_by_text("등록된 게시글이 없습니다.")).to_be_visible()
            assert rows() == []
            browser.close()
    finally:
        server.shutdown()
        worker.join(timeout=3)
        server.server_close()
