from logidoor.new_libs.mechanicalsoup import stateful_browser


class Form:
    def __init__(self):
        self.method = ""
        self.action = ""
        self.name = ""
        self.entry_text = []
        self.entry_password = []
        self.submit_button = []


class Browser(stateful_browser.StatefulBrowser):
    def __init__(self, *args, **kwargs):
        self.login_form = None
        super().__init__(*args, **kwargs)

    def find_login_form(self):
        for form in self.page.find_all("form"):
            current_form = Form()
            current_form.name = form.get('name')
            current_form.method = form.get('method')
            current_form.action = form.get('action')
            for entry in form.find_all(("input", "textarea", "select", "button")):
                entry_type = entry.get('type')
                if entry_type == "text":
                    current_form.entry_text.append((entry.get('id'), entry.get('name')))
                elif entry_type == "password":
                    current_form.entry_password.append((entry.get('id'), entry.get('name')))
                elif entry_type == "submit":
                    current_form.submit_button.append((entry.get('id'), entry.get('name'), entry.get('value')))

            if len(current_form.entry_password) == 1:
                return current_form
        return False

    def login(self, username="", password=""):
        if self.login_form.name:
            self.select_form(f"form[name=\"{self.login_form.name}\"]")
        elif self.login_form.action:
            self.select_form(f"form[action=\"{self.login_form.action}\"]")
        elif self.login_form.method:
            self.select_form(f"form[method=\"{self.login_form.method}\"]")
        else:
            raise AttributeError("Login form has no name, action or method to select")

        if self.login_form.entry_text:
            entry = self.login_form.entry_text[0][0] if self.login_form.entry_text[0][0] else\
                self.login_form.entry_text[0][1]
            self[entry] = username

        entry = self.login_form.entry_password[0][0] if self.login_form.entry_password[0][0] else \
            self.login_form.entry_password[0][1]
        self[entry] = password

        return self.submit_selected()
