import re
from logidoor.libs.mechanicalsoup import stateful_browser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import html2text


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
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.login_form = None
        self.first_page = ""
        self.first_title = ""
        self.first_content = ""
        # self.first_content = ""
        self.blacklist_extensions = (
            ".css", ".js", ".jpg", ".png", ".jpeg", ".doc", ".docx", ".xlsx", ".pdf", ".txt", ".rar", ".bak", ".zip",
            ".7z")
        super().__init__(*args, **kwargs)

    def auto_set_proxy(self, proxy):
        if not proxy:
            pass
        else:
            self.session.proxies = proxy

    def auto_set_ua(self):
        # TODO generate random UserAgent here
        pass

    # def count_page_contents_urls(self, resp):
    #     convert = html2text.HTML2Text()
    #     convert.handle(resp)
    #     return convert.outcount

    def get_page_contents(self, resp, ignore_links=False):
        convert = html2text.HTML2Text()
        convert.ignore_links = ignore_links
        contents = [x for x in convert.handle(resp).split("\n") if x.strip()]
        return contents

    def get_page_first_contents(self, resp):
        self.first_content = self.get_page_contents(resp)

    def find_login_form(self):
        try:
            for form in self.page.find_all("form"):
                current_form = Form()
                current_form.name = form.get('name')
                current_form.method = form.get('method')
                current_form.action = form.get('action')
                for entry in form.find_all(("input", "textarea", "select", "button")):
                    entry_type = entry.get('type')
                    if entry_type.lower() == "text":
                        current_form.entry_text.append((entry.get('id'), entry.get('name')))
                    elif entry_type.lower() == "password":
                        current_form.entry_password.append((entry.get('id'), entry.get('name')))
                    elif entry_type.lower() == "submit":
                        current_form.submit_button.append((entry.get('id'), entry.get('name'), entry.get('value')))

                if len(current_form.entry_password) == 1:
                    return current_form
        except AttributeError:
            return False
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
            entry = self.login_form.entry_text[0][1] if self.login_form.entry_text[0][1] else \
                self.login_form.entry_text[0][0]
            self[entry] = username

        entry = self.login_form.entry_password[0][1] if self.login_form.entry_password[0][1] else \
            self.login_form.entry_password[0][0]
        self[entry] = password

        return self.submit_selected()

    def get_page_redirection(self, data, check_url):
        from urllib import parse as urlparse
        """
            Analysis all redirection request in html response via meta tag, windows.location or href
            :return: list of string = all possible URL
        """
        regex_js = r"[window\.]?location(?:.*)=[ \'\"]?([a-zA-Z\._\/]+)[ \'\"]?"
        regex_meta = r"<meta[^>]*?url=(.*?)[\"\']"
        regex_href = r"href=[\'\"]?([^\'\" >]+)"
        url = list(set(re.findall(regex_meta, data)))
        url += list(set(re.findall(regex_js, data)))
        url += list(set(re.findall(regex_href, data)))
        for current_url in url:
            to_check_url = current_url
            if not to_check_url.startswith("http"):
                # URL can be Absolute URLs vs. Relative URLs
                # When URL is Relative, we can use urljoin as stackoverflow bellow
                # from urllib.parse import urljoin
                # check_url = urljoin(url, this_url)
                # https://stackoverflow.com/a/44002598
                # Or use open_relative which is mentioned in the doc, follow_link part
                to_check_url = urlparse.urljoin(check_url, to_check_url)
            if not urlparse.urlparse(to_check_url).path.endswith(self.blacklist_extensions) and \
                    urlparse.urlparse(to_check_url).netloc == urlparse.urlparse(check_url).netloc and \
                    urlparse.urlparse(to_check_url).path != urlparse.urlparse(check_url).path:
                yield to_check_url

    def get_page_change(self, text):
        result = ""
        for line in text.split("\n"):
            if line not in self.first_page:
                result += line + "\n"

        return result
