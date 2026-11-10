async def run_test(page, output_dir, page_url):
    import traceback

    try:
        await page.set_viewport_size({"width": 1920, "height": 1080})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        await page.goto("https://gta6-menu--27zgavcg.preview.emergentagent.com", wait_until="networkidle", timeout=30000)
        await page.wait_for_selector('[data-testid="hero-title"]', timeout=10000)
        assert await page.locator('[data-testid="hero-title"]').inner_text()
        assert await page.locator('[data-testid="api-status"]').inner_text() == "API / ONLINE"
        print("PASS: hero and API online status loaded")

        await page.locator('[data-testid="hamburger-menu-button"]').scroll_into_view_if_needed()
        await page.locator('[data-testid="hamburger-menu-button"]').click()
        await page.wait_for_selector('[data-testid="hamburger-menu-panel"]', state="visible")
        print("PASS: hamburger menu opens")
        for testid, section in [("menu-story-link", "story-section"), ("menu-characters-link", "characters-section"), ("menu-eggs-link", "easter-eggs-section"), ("menu-trailers-link", "trailers-section")]:
            await page.locator(f'[data-testid="{testid}"]').click()
            await page.wait_for_timeout(250)
            assert await page.locator(f'[data-testid="{section}"]').is_visible()
            if testid != "menu-trailers-link":
                await page.locator('[data-testid="hamburger-menu-button"]').click()
                await page.wait_for_selector('[data-testid="hamburger-menu-panel"]', state="visible")
        await page.locator('[data-testid="close-menu-button"]').click()
        await page.wait_for_selector('[data-testid="hamburger-menu-panel"]', state="hidden")
        print("PASS: all menu links navigate and menu closes")

        await page.locator('[data-testid="characters-section"]').scroll_into_view_if_needed()
        initial_name = await page.locator('[data-testid="active-character-name"]').inner_text()
        await page.locator('[data-testid="character-switch-jason"]').click()
        await page.wait_for_timeout(600)
        assert initial_name == "Lucia"
        assert await page.locator('[data-testid="active-character-name"]').inner_text() == "Jason"
        assert await page.locator('[data-testid="active-character-image"]').get_attribute("alt") == "Jason"
        print("PASS: character switch updates name and image")

        await page.locator('[data-testid="easter-eggs-section"]').scroll_into_view_if_needed()
        await page.locator('[data-testid="egg-filter-teoria"]').click()
        await page.wait_for_timeout(350)
        cards = page.locator('[data-testid^="easter-egg-card-"]')
        assert await cards.count() == 1
        assert await cards.first.locator('.tag').inner_text() == "TEORIA"
        await page.locator('[data-testid="egg-filter-todos"]').click()
        await page.wait_for_timeout(350)
        assert await cards.count() == 3
        print("PASS: easter egg filters update cards")

        await page.locator('[data-testid="trailers-section"]').scroll_into_view_if_needed()
        initial_title = await page.locator('[data-testid="trailer-card"] h3').inner_text() if await page.locator('[data-testid="trailer-card"] h3').count() else await page.locator('.trailer-overlay h3').inner_text()
        initial_src = await page.locator('[data-testid="active-trailer-image"]').get_attribute("src")
        await page.locator('[data-testid="trailer-next-button"]').click()
        await page.wait_for_timeout(450)
        assert await page.locator('.trailer-overlay h3').inner_text() != initial_title
        assert await page.locator('[data-testid="active-trailer-image"]').get_attribute("src") != initial_src
        print("PASS: trailer next control updates title and image")

        overflow = await page.evaluate("""() => ({scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth})""")
        assert overflow["scrollWidth"] <= overflow["innerWidth"] + 2, overflow
        print("PASS: desktop has no horizontal overflow")

        await page.set_viewport_size({"width": 390, "height": 844})
        await page.reload(wait_until="networkidle")
        await page.wait_for_selector('[data-testid="hero-title"]', timeout=10000)
        mobile_overflow = await page.evaluate("""() => ({scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth})""")
        assert mobile_overflow["scrollWidth"] <= mobile_overflow["innerWidth"] + 2, mobile_overflow
        await page.locator('[data-testid="hamburger-menu-button"]').click()
        await page.wait_for_selector('[data-testid="hamburger-menu-panel"]', state="visible")
        assert await page.locator('[data-testid="menu-trailers-link"]').is_visible()
        await page.locator('[data-testid="close-menu-button"]').click()
        print("PASS: mobile loads, menu remains usable, and has no horizontal overflow")

        error_text = await page.evaluate("""() => {
          const errorElements = Array.from(document.querySelectorAll('.error, [class*="error"], [id*="error"]'));
          return errorElements.map(el => el.textContent).join(", ");
        }""")
        if error_text:
            print(f"Found error message: {error_text}")
        else:
            print("No error messages found on the page")
        assert not console_errors, console_errors
        print("PASS: no browser console errors or page error messages")
    except AssertionError as exc:
        print(f"FINDING: assertion failed: {exc}")
        traceback.print_exc()
    except Exception as exc:
        print(f"FINDING: UI test execution failed: {exc}")
        traceback.print_exc()
