from pytest_bdd import given, scenarios, then, when

scenarios("../message_list.feature")


# for some reason, if I don't instantiate the
# browser before the message, it isn't added
@given("A message exists", target_fixture="message")
def message_exists(browser, test_message):
    test_message.save()
    return test_message


@when("User visits the message list page", target_fixture="page")
def user_visits_messages_page(db, browser):
    browser.visit(browser.domain + browser.pages["list_message"])
    return browser


@then("The message is listed")
def message_is_listed(message, page):
    page.assert_element(f"a[href='/{message.id}/{message.slug}/']")
