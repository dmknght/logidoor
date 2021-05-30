import re
from logidoor.libs.mechanicalsoup import stateful_browser


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
        self.first_page = ""
        self.first_title = ""
        self.blacklist_extensions = (
            ".css", ".js", ".jpg", ".png", ".jpeg", ".doc", ".docx", ".xlsx", ".pdf", ".txt", ".rar", ".bak", ".zip",
            ".7z"
        )
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
            entry = self.login_form.entry_text[0][1] if self.login_form.entry_text[0][1] else\
                self.login_form.entry_text[0][0]
            self[entry] = username

        entry = self.login_form.entry_password[0][1] if self.login_form.entry_password[0][1] else \
            self.login_form.entry_password[0][0]
        self[entry] = password

        return self.submit_selected()

    def page_redirection(self):
        """
            Analysis all redirection request in html response via meta tag, windows.location or href
            :return: list of string = all possible URL
            """
        regex_js = r"[window\.]?location(?:.*)=[ \'\"]?([a-zA-Z\._\/]+)[ \'\"]?"
        regex_meta = r"<meta[^>]*?url=(.*?)[\"\']"
        regex_href = r"href=[\'\"]?([^\'\" >]+)"

        url = list(set(re.findall(regex_meta, self.page)))
        if url:
            return url

        url = list(set(re.findall(regex_js, self.page)))
        if url:
            return url

        url = list(set(re.findall(regex_href, self.page)))
        return url

    def check_login_redirection(self):
        for new_url in self.page_redirection():
            if not new_url.endswith(self.blacklist_extensions):  # maybe it can be URL of file with args
                self.open(new_url)
                if self.find_login_form():
                    return True
        return False
