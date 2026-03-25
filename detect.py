# Coded By Umut Özen
import requests
import os
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "report.html")

def get_form_details(form):
    print(f"{Fore.BLUE}Form:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Action:{Style.RESET_ALL}", form.get('action'))
    print(f"{Fore.GREEN}Method:{Style.RESET_ALL}", form.get('method'))

    inputs = form.find_all('input')
    for input_element in inputs:
        print(f"{Fore.YELLOW}Input:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Type:{Style.RESET_ALL}",  input_element.get('type'))
        print(f"{Fore.CYAN}Name:{Style.RESET_ALL}",  input_element.get('name'))
        print(f"{Fore.CYAN}Value:{Style.RESET_ALL}", input_element.get('value'))
        print("------")

def build_form_html(form, url):
    action = form.get('action') or None
    method = form.get('method') or None
    inputs = form.find_all('input')

    action_html = action if action else '<span class="null">—</span>'
    method_html = method if method else '<span class="null">—</span>'

    rows = ""
    for inp in inputs:
        t = inp.get('type')  or "—"
        n = inp.get('name')  or "—"
        v = inp.get('value') or "—"
        rows += f"<tr><td>{t}</td><td>{n}</td><td>{v}</td></tr>"

    if inputs:
        table = f"""
        <table>
            <thead><tr><th>Type</th><th>Name</th><th>Value</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""
    else:
        table = '<p class="no-inputs">No input elements found in this form.</p>'

    return f"""
    <div class="form-card">
        <div class="form-card-header">
            <span class="badge">FORM</span>
            <span class="form-url">{url}</span>
        </div>
        <div class="form-meta">
            <div class="meta-cell">
                <span class="cell-label">Action</span>
                <span class="cell-value {'null' if not action else ''}">{action_html}</span>
            </div>
            <div class="meta-cell">
                <span class="cell-label">Method</span>
                <span class="cell-value {'null' if not method else ''}">{method_html}</span>
            </div>
        </div>
        {table}
    </div>"""

def generate_html_report(url, forms, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = os.path.join(output_dir, f"report_{timestamp}.html")
    scan_date = datetime.now().strftime("%B %d, %Y  %H:%M:%S")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    if forms:
        forms_body = "".join([build_form_html(frm, url) for frm in forms])
    else:
        forms_body = '<div class="empty-notice">No forms were found on this page.</div>'

    html = (template
            .replace("{{URL}}",        url)
            .replace("{{FORM_COUNT}}", str(len(forms)))
            .replace("{{SCAN_DATE}}",  scan_date)
            .replace("{{FORMS_BODY}}", forms_body))

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename

def main():
    url = input("Please enter the URL: ")

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/91.0.4472.124 Safari/537.36')
    }
    response = requests.get(url, headers=headers)

    soup  = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        get_form_details(form)
        print(f"{Fore.MAGENTA}URL:{Style.RESET_ALL}", url)
        print("===================")

    report_path = generate_html_report(url, forms)
    abs_path    = os.path.abspath(report_path)
    print(f"\n{Fore.GREEN}✔ Report saved:{Style.RESET_ALL} {abs_path}")
    webbrowser.open(f"file:///{abs_path}")

if __name__ == "__main__":
    main()
