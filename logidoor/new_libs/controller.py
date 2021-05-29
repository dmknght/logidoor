def do_attack(browser, prog_options):
    for username in prog_options.userlist:
        for password in prog_options.passlist:
            resp = browser.login(username, password)
            # TODO analysis more from here
            if not browser.find_login_form():
                if browser.login_form.entry_text:
                    print(f"Found: {username}:{password}")
                else:
                    print(f"Found: {password}")
                return
