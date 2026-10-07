from pathlib import Path

from playwright.sync_api import expect, sync_playwright
import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]


def login(page):
    page.get_by_label('아이디', exact=True).fill('tester')
    page.get_by_label('비밀번호', exact=True).fill('temporary-test-password')
    page.get_by_role('button', name='대시보드 열기').click()
    expect(page.get_by_role('heading', name='오늘의 서비스 관찰')).to_be_visible()
    expect(page.get_by_role('button', name='목록 새로고침')).to_be_enabled()


@pytest.mark.browser
@pytest.mark.parametrize('width,height', [(1440, 1080), (390, 844)])
def test_complete_dashboard_flow(frontend, width, height):
    url, monitor_url, general_url = frontend
    result = requests.post(general_url + '/board/new', data={'title': '브라우저 게시글', 'body': '관찰할 내용'}, allow_redirects=False, timeout=5)
    assert result.status_code == 303
    requests.get(general_url + result.headers['Location'], timeout=5)
    requests.get(general_url + '/board/2147483647', timeout=5)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height}, locale='ko-KR')
        page_errors = []
        page.on('pageerror', lambda error: page_errors.append(str(error)))
        page.goto(url)
        page.get_by_label('아이디', exact=True).fill('tester')
        page.get_by_label('비밀번호', exact=True).fill('incorrect')
        page.get_by_role('button', name='대시보드 열기').click()
        expect(page.get_by_role('alert')).to_contain_text('올바르지 않습니다')
        login(page)
        expect(page.get_by_role('table')).to_contain_text('/board/2147483647')
        expect(page.get_by_role('table')).to_contain_text('404')
        expect(page.get_by_role('heading', name='관찰 메모 0')).to_be_visible()
        # Refresh both lists after a new real board request.
        requests.get(general_url + '/board/2147483646', timeout=5)
        page.get_by_role('button', name='목록 새로고침').click()
        expect(page.get_by_role('table')).to_contain_text('/board/2147483646')
        page.get_by_label('요청 경로 검색').fill('/board/2147483647')
        expect(page.locator('tbody tr')).to_have_count(1)
        expect(page.locator('.stat-card').nth(0).locator('strong')).to_have_text('1건')
        expect(page.locator('.stat-card').nth(1).locator('strong')).to_have_text('1건')
        page.get_by_role('button', name='필터 초기화').click()
        page.get_by_label('응답 상태 필터').select_option('success')
        expect(page.locator('.stat-card').nth(1).locator('strong')).to_have_text('0건')
        page.get_by_role('button', name='필터 초기화').click()
        # Create: server handles blank inputs; preserve what the operator typed.
        page.get_by_role('button', name='새 메모').click()
        page.get_by_label('제목', exact=True).fill('  관찰 한 개  ')
        page.get_by_label('내용', exact=True).fill('   ')
        page.get_by_role('button', name='메모 저장').click()
        expect(page.get_by_role('alert')).to_contain_text('제목과 내용을 확인')
        expect(page.get_by_label('제목', exact=True)).to_have_value('  관찰 한 개  ')
        assert requests.get(monitor_url + '/api/notes', timeout=5).json()['notes'] == []
        page.get_by_label('내용', exact=True).fill('  404 응답을 확인했습니다.  ')
        page.get_by_role('button', name='메모 저장').click()
        expect(page.get_by_role('heading', name='관찰 한 개', exact=True)).to_be_visible()
        expect(page.locator('.note-body')).to_have_text('404 응답을 확인했습니다.')
        # Editing starts with persisted values, invalid PUT preserves DB.
        page.get_by_role('button', name='수정', exact=True).click()
        expect(page.get_by_label('제목', exact=True)).to_have_value('관찰 한 개')
        expect(page.get_by_label('내용', exact=True)).to_have_value('404 응답을 확인했습니다.')
        page.get_by_label('내용', exact=True).fill(' \n ')
        page.get_by_role('button', name='메모 저장').click()
        expect(page.get_by_role('alert')).to_contain_text('제목과 내용을 확인')
        note_id = requests.get(monitor_url + '/api/notes', timeout=5).json()['notes'][0]['id']
        assert requests.get(monitor_url + f'/api/notes/{note_id}', timeout=5).json()['note']['body'] == '404 응답을 확인했습니다.'
        page.get_by_role('button', name='취소', exact=True).click()
        expect(page.locator('.note-body')).to_have_text('404 응답을 확인했습니다.')
        page.get_by_role('button', name='수정', exact=True).click()
        page.get_by_label('제목', exact=True).fill('수정된 관찰')
        page.get_by_label('내용', exact=True).fill('수정 내용이 DB에 유지됩니다.')
        page.get_by_role('button', name='메모 저장').click()
        expect(page.get_by_role('heading', name='수정된 관찰', exact=True)).to_be_visible()
        expect(page.locator('.note-list')).to_contain_text('수정된 관찰')
        # A second note: cancel must keep it, confirm must delete only it.
        page.get_by_role('button', name='새 메모').click()
        page.get_by_label('제목', exact=True).fill('삭제 시험 메모')
        page.get_by_label('내용', exact=True).fill('삭제 취소와 확정 확인')
        page.get_by_role('button', name='메모 저장').click()
        expect(page.get_by_role('heading', name='삭제 시험 메모', exact=True)).to_be_visible()
        page.get_by_role('button', name='삭제', exact=True).click()
        expect(page.get_by_role('heading', name='이 메모를 삭제할까요?')).to_be_visible()
        page.get_by_role('button', name='취소', exact=True).click()
        expect(page.get_by_role('heading', name='삭제 시험 메모', exact=True)).to_be_visible()
        assert len(requests.get(monitor_url + '/api/notes', timeout=5).json()['notes']) == 2
        page.get_by_role('button', name='삭제', exact=True).click()
        page.get_by_role('button', name='삭제 확정').click()
        expect(page.get_by_role('status')).to_contain_text('삭제했습니다')
        expect(page.locator('.note-list')).not_to_contain_text('삭제 시험 메모')
        # Reload clears user state while notes/events remain in PostgreSQL.
        page.reload()
        expect(page.get_by_role('heading', name='운영자 로그인')).to_be_visible()
        login(page)
        page.locator('.note-list').get_by_role('button', name='수정된 관찰', exact=False).click()
        expect(page.locator('.note-body')).to_have_text('수정 내용이 DB에 유지됩니다.')
        expect(page.locator('.note-list')).not_to_contain_text('삭제 시험 메모')
        # React displays backend/network failures without false success.
        page.route('**/api/notes', lambda route: route.fulfill(status=503, content_type='application/json', body='{"error":"메모 조회 실패 테스트"}'))
        page.get_by_role('button', name='목록 새로고침').click()
        expect(page.locator('.note-list').get_by_role('alert')).to_contain_text('메모 조회 실패 테스트')
        page.unroute('**/api/notes')
        page.route('**/api/events', lambda route: route.abort('failed'))
        page.get_by_role('button', name='목록 새로고침').click()
        expect(page.locator('.events-panel').get_by_role('alert')).to_contain_text('서버에 연결하지 못했습니다')
        page.unroute('**/api/events')
        page.get_by_role('button', name='목록 새로고침').click()
        expect(page.locator('.events-panel').get_by_role('alert')).to_have_count(0)
        expect(page.get_by_role('button', name='목록 새로고침')).to_be_enabled()
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        assert not page_errors
        cache = ROOT / '.cache'
        cache.mkdir(exist_ok=True)
        page.screenshot(path=str(cache / f'dashboard-{width}.png'), full_page=True)
        page.get_by_role('button', name='로그아웃').click()
        expect(page.get_by_role('heading', name='운영자 로그인')).to_be_visible()
        page.screenshot(path=str(cache / f'login-{width}.png'), full_page=True)
        browser.close()
