import calendar
import json
import os
import webbrowser
from datetime import date

from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu

try:
    from kivymd.uix.pickers import MDModalDatePicker
except ImportError:
    MDModalDatePicker = None  # type: ignore[misc, assignment]
    from kivymd.uix.pickers import MDDatePicker
else:
    MDDatePicker = None  # type: ignore[misc, assignment]

from kivymd.uix.tab import MDTabsItemText, MDTabsPrimary

SOURCE_CODE_URL = "https://github.com/Tumanchi/mortgage-calculator.git"
PREFS_FILENAME = "mortgage_app_settings.json"

STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "tab_input": "Ввод",
        "tab_table": "Таблица",
        "tab_graph": "График",
        "tab_chart": "Диаграмма",
        "tab_sum": "Итоги",
        "nav_app": "Калькулятор ипотеки",
        "nav_menu": "Меню навигации",
        "nav_sections": "Разделы",
        "nav_calc": "Расчёт ипотеки",
        "nav_charts": "Графики и диаграммы",
        "nav_source": "Исходный код",
        "nav_extra": "Дополнительно",
        "nav_about": "О приложении",
        "nav_appearance": "Оформление",
        "nav_theme_light": "Светлая тема",
        "nav_theme_dark": "Тёмная тема",
        "nav_language": "Язык",
        "nav_lang_ru": "Русский",
        "nav_lang_en": "English",
        "params_title": "Параметры кредита",
        "hint_start_date": "Дата начала",
        "hint_property_price": "Стоимость недвижимости, KZT",
        "hint_term_years": "Срок кредита, лет",
        "hint_loan_amount": "Сумма кредита, KZT",
        "hint_down_payment": "Первоначальный взнос, KZT",
        "hint_rate": "Ставка, % годовых",
        "hint_payment_type": "Тип платежа",
        "btn_calculate": "Рассчитать",
        "results_title": "Результаты расчёта",
        "dash": "—",
        "err_numeric": "Ошибка: проверьте числовые поля",
        "res_payment_none": "Платёж: —",
        "res_interest_none": "Переплата по процентам: —",
        "res_total_none": "Общая сумма выплат: —",
        "res_eff": "Эффективная ставка (год): {pct}",
        "res_monthly_annuity": "Ежемесячный платёж: {amt}",
        "res_monthly_diff": "Платёж: {first} (1-й мес.) → {last} (последний)",
        "table_title": "Таблица — график платежей",
        "graph_title": "График платежей",
        "graph_subtitle": "Столбцы: проценты (красный) и тело платежа (синий) по месяцам",
        "legend_interest": "Проценты",
        "legend_principal": "Основной",
        "chart_title": "Совокупные выплаты",
        "chart_subtitle": "Круговая диаграмма: доля процентов и тела в общей сумме выплат",
        "sum_title": "Сводка по кредиту",
        "sum_subtitle": "Данные после нажатия «Рассчитать» на вкладке «Ввод».",
        "sum_principal": "Сумма кредита: {v}",
        "sum_term": "Срок: {months} мес. ({years} г.)",
        "sum_rate": "Ставка: {pct} годовых",
        "sum_type": "Тип платежа: {t}",
        "sum_monthly": "Платёж (показатель): {v}",
        "sum_interest": "Переплата по процентам: {v}",
        "sum_total": "Общая сумма выплат: {v}",
        "sum_eff": "Эффективная ставка (год): {pct}",
        "sum_empty": "Нет данных — выполните расчёт на вкладке «Ввод».",
        "pay_annuity": "Аннуитетный",
        "pay_diff": "Дифференцированный",
        "about_title": "О приложении",
        "about_ok": "OK",
        "about_body": (
            "Ипотечный калькулятор на Python (Kivy / KivyMD).\n"
            "Версия интерфейса 1.3. Исходный код на GitHub."
        ),
        "app_title": "Mortgage Calculator",
        "col_no": "№",
        "col_date": "Дата",
        "col_payment": "Платёж",
        "col_interest": "Проценты",
        "col_principal": "Основной",
        "col_balance": "Остаток",
    },
    "en": {
        "tab_input": "Input",
        "tab_table": "Table",
        "tab_graph": "Graph",
        "tab_chart": "Chart",
        "tab_sum": "Summary",
        "nav_app": "Mortgage calculator",
        "nav_menu": "Navigation",
        "nav_sections": "Sections",
        "nav_calc": "Mortgage calculation",
        "nav_charts": "Charts",
        "nav_source": "Source code",
        "nav_extra": "More",
        "nav_about": "About",
        "nav_appearance": "Appearance",
        "nav_theme_light": "Light theme",
        "nav_theme_dark": "Dark theme",
        "nav_language": "Language",
        "nav_lang_ru": "Russian",
        "nav_lang_en": "English",
        "params_title": "Loan parameters",
        "hint_start_date": "Start date",
        "hint_property_price": "Property price, KZT",
        "hint_term_years": "Loan term, years",
        "hint_loan_amount": "Loan amount, KZT",
        "hint_down_payment": "Down payment, KZT",
        "hint_rate": "Interest rate, % p.a.",
        "hint_payment_type": "Payment type",
        "btn_calculate": "Calculate",
        "results_title": "Results",
        "dash": "—",
        "err_numeric": "Error: check numeric fields",
        "res_payment_none": "Payment: —",
        "res_interest_none": "Interest overpayment: —",
        "res_total_none": "Total paid: —",
        "res_eff": "Effective annual rate: {pct}",
        "res_monthly_annuity": "Monthly payment: {amt}",
        "res_monthly_diff": "Payment: {first} (1st mo.) → {last} (last mo.)",
        "table_title": "Payment schedule (table)",
        "graph_title": "Payment chart",
        "graph_subtitle": "Bars: interest (red) and principal (blue) by month",
        "legend_interest": "Interest",
        "legend_principal": "Principal",
        "chart_title": "Total payments",
        "chart_subtitle": "Pie chart: interest vs principal share of total paid",
        "sum_title": "Loan summary",
        "sum_subtitle": "Data after you tap Calculate on the Input tab.",
        "sum_principal": "Loan amount: {v}",
        "sum_term": "Term: {months} mo. ({years} yr.)",
        "sum_rate": "Rate: {pct} p.a.",
        "sum_type": "Payment type: {t}",
        "sum_monthly": "Payment (indicator): {v}",
        "sum_interest": "Interest overpayment: {v}",
        "sum_total": "Total paid: {v}",
        "sum_eff": "Effective annual rate: {pct}",
        "sum_empty": "No data — run calculation on the Input tab.",
        "pay_annuity": "Annuity",
        "pay_diff": "Differentiated",
        "about_title": "About",
        "about_ok": "OK",
        "about_body": (
            "Mortgage calculator (Python, Kivy / KivyMD).\n"
            "UI version 1.3. Source on GitHub."
        ),
        "app_title": "Mortgage Calculator",
        "col_no": "#",
        "col_date": "Date",
        "col_payment": "Payment",
        "col_interest": "Interest",
        "col_principal": "Principal",
        "col_balance": "Balance",
    },
}


def _fmt_rub(value: float) -> str:
    """Format amount as integer rubles with spaces as thousands separators."""
    s = f"{round(value):,}".replace(",", " ")
    return f"{s} KZT"


def _fmt_pct(value: float) -> str:
    return f"{value:.2f} %"


def _parse_start_date(raw: str) -> date | None:
    raw = (raw or "").strip().replace("/", ".")
    if not raw:
        return None
    parts = raw.split(".")
    if len(parts) != 3:
        return None
    try:
        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
        return date(y, m, d)
    except (ValueError, OverflowError):
        return None


def _monthly_rate_percent(annual_percent: float) -> float:
    """Monthly rate as decimal (e.g. 0.007916 for 9.5% p.a.)."""
    return (annual_percent / 100.0) / 12.0


def _annuity_monthly_payment(principal: float, annual_percent: float, n_months: int) -> float:
    if n_months <= 0 or principal <= 0:
        return 0.0
    i = _monthly_rate_percent(annual_percent)
    if i <= 0:
        return principal / n_months
    pow_term = (1.0 + i) ** n_months
    return principal * (i * pow_term) / (pow_term - 1.0)


def _effective_annual_percent(nominal_annual_percent: float) -> float:
    """EAR from nominal annual rate with monthly compounding (lesson-style headline rate)."""
    i = _monthly_rate_percent(nominal_annual_percent)
    if i <= 0:
        return 0.0
    return 100.0 * ((1.0 + i) ** 12 - 1.0)


def _totals_annuity(principal: float, annual_percent: float, n_months: int) -> tuple[float, float, float]:
    """Returns (monthly_payment, total_interest, total_paid)."""
    monthly = _annuity_monthly_payment(principal, annual_percent, n_months)
    total_paid = monthly * n_months
    return monthly, max(0.0, total_paid - principal), total_paid


def add_calendar_months(origin: date, months: int) -> date:
    """Add calendar months with day clamped to last day of month (lesson-style next-month stepping)."""
    y = origin.year + (origin.month - 1 + months) // 12
    m = (origin.month - 1 + months) % 12 + 1
    d = min(origin.day, calendar.monthrange(y, m)[1])
    return date(y, m, d)


def _totals_differentiated(principal: float, annual_percent: float, n_months: int) -> tuple[float, float, float, float]:
    """
    Returns (first_month_payment, last_month_payment, total_interest, total_paid).
    """
    if n_months <= 0 or principal <= 0:
        return 0.0, 0.0, 0.0, 0.0
    i = _monthly_rate_percent(annual_percent)
    principal_part = principal / n_months
    balance = principal
    total_interest = 0.0
    total_paid = 0.0
    first_pay = 0.0
    last_pay = 0.0
    for month_idx in range(n_months):
        interest = balance * i
        pay = principal_part + interest
        total_interest += interest
        total_paid += pay
        balance -= principal_part
        if month_idx == 0:
            first_pay = pay
        last_pay = pay
    return first_pay, last_pay, total_interest, total_paid


def _schedule_annuity_rows(
    principal: float, annual_percent: float, n_months: int, start: date
) -> list[tuple[int, date, float, float, float, float]]:
    """Each row: month_no, pay_date, payment, interest, principal_part, balance_after."""
    i = _monthly_rate_percent(annual_percent)
    monthly = _annuity_monthly_payment(principal, annual_percent, n_months)
    balance = principal
    rows: list[tuple[int, date, float, float, float, float]] = []
    for month_no in range(1, n_months + 1):
        pay_date = add_calendar_months(start, month_no - 1)
        interest = balance * i
        if month_no == n_months:
            principal_part = balance
            payment = principal_part + interest
        else:
            payment = monthly
            principal_part = payment - interest
        balance -= principal_part
        rows.append((month_no, pay_date, payment, interest, principal_part, max(balance, 0.0)))
    return rows


def _schedule_differentiated_rows(
    principal: float, annual_percent: float, n_months: int, start: date
) -> list[tuple[int, date, float, float, float, float]]:
    i = _monthly_rate_percent(annual_percent)
    principal_part = principal / n_months
    balance = principal
    rows: list[tuple[int, date, float, float, float, float]] = []
    for month_no in range(1, n_months + 1):
        pay_date = add_calendar_months(start, month_no - 1)
        interest = balance * i
        payment = principal_part + interest
        balance -= principal_part
        rows.append((month_no, pay_date, payment, interest, principal_part, max(balance, 0.0)))
    return rows


def payment_type_is_diff(display: str) -> bool:
    """True if the payment type field matches differentiated label in any supported language."""
    d = (display or "").strip()
    return d in (STRINGS["ru"]["pay_diff"], STRINGS["en"]["pay_diff"])


def _schedule_table_row_widget(
    texts: tuple[str, str, str, str, str, str],
    row_bg: tuple[float, float, float, float],
    header: bool = False,
) -> MDBoxLayout:
    """One horizontal row for MDList (lesson: several labels in one line)."""
    widths = (0.1, 0.18, 0.2, 0.18, 0.17, 0.17)
    row = MDBoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=dp(40),
        spacing=dp(2),
        padding=(dp(4), 0),
        md_bg_color=row_bg,
    )
    for text, w in zip(texts, widths):
        row.add_widget(
            MDLabel(
                text=text,
                bold=header,
                halign="center",
                valign="middle",
                size_hint_x=w,
                shorten=True,
                shorten_from="right",
            )
        )
    return row


# Tabs + first-tab form live in KV below (lesson: declarative UI, no programmatic tab loop).
KV = """
#:import Clock kivy.clock.Clock
#:import dp kivy.metrics.dp
#:import CheckBox kivy.uix.checkbox.CheckBox

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:

            MDScreen:
                name: "main"

                MDBoxLayout:
                    orientation: "vertical"
                    # Toolbar is MDTopAppBar (~56dp small); tabs sit flush below it like Material layout
                    padding: 0, dp(56), 0, 0
                    spacing: 0

                    MDTabsPrimary:
                        id: main_tabs
                        size_hint_y: 1
                        indicator_anim: False

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "view-grid-outline"
                            MDTabsItemText:
                                id: tab_text_input
                                text: "Ввод"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "table"
                            MDTabsItemText:
                                id: tab_text_table
                                text: "Таблица"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "chart-line"
                            MDTabsItemText:
                                id: tab_text_graph
                                text: "График"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "chart-pie"
                            MDTabsItemText:
                                id: tab_text_chart
                                text: "Диаграмма"

                        MDTabsItem:
                            MDTabsItemIcon:
                                icon: "book-open-variant"
                            MDTabsItemText:
                                id: tab_text_sum
                                text: "Итоги"

                        MDDivider:

                        MDTabsCarousel:
                            id: tab_carousel
                            size_hint_y: 1

                            MDScrollView:
                                do_scroll_x: False
                                size_hint: 1, 1

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: dp(12)
                                    padding: dp(16)
                                    size_hint_y: None
                                    height: self.minimum_height

                                    MDLabel:
                                        id: label_params_title
                                        text: "Параметры кредита"
                                        adaptive_height: True
                                        bold: True

                                    MDTextField:
                                        id: field_start_date
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        on_focus: if self.focus: app.open_start_date_picker()
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar"
                                        MDTextFieldHintText:
                                            id: hint_start_date
                                            text: "Дата начала"

                                    # Like reference: stacked filled fields with hint only (no persistent helper).
                                    MDTextField:
                                        id: field_property_price
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "home-variant-outline"
                                        MDTextFieldHintText:
                                            id: hint_property_price
                                            text: "Стоимость недвижимости, KZT"

                                    MDTextField:
                                        id: field_term_years
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "int"
                                        MDTextFieldLeadingIcon:
                                            icon: "calendar-clock"
                                        MDTextFieldHintText:
                                            id: hint_term_years
                                            text: "Срок кредита, лет"

                                    MDTextField:
                                        id: field_loan_amount
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "cash"
                                        MDTextFieldHintText:
                                            id: hint_loan_amount
                                            text: "Сумма кредита, KZT"

                                    MDTextField:
                                        id: field_down_payment
                                        mode: "filled"
                                        size_hint_y: None
                                        height: self.minimum_height
                                        input_filter: "float"
                                        MDTextFieldLeadingIcon:
                                            icon: "wallet-outline"
                                        MDTextFieldHintText:
                                            id: hint_down_payment
                                            text: "Первоначальный взнос, KZT"

                                    # Bottom row: icon on the left field only (same pattern as Interest / Payment type).
                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(8)
                                        size_hint_y: None
                                        height: self.minimum_height

                                        MDTextField:
                                            id: field_rate
                                            mode: "filled"
                                            size_hint_x: 0.5
                                            size_hint_y: None
                                            height: self.minimum_height
                                            input_filter: "float"
                                            MDTextFieldLeadingIcon:
                                                icon: "bank"
                                            MDTextFieldHintText:
                                                id: hint_rate
                                                text: "Ставка, % годовых"

                                        MDTextField:
                                            id: field_payment_type
                                            mode: "filled"
                                            size_hint_x: 0.5
                                            size_hint_y: None
                                            height: self.minimum_height
                                            on_focus: if self.focus: app.open_payment_type_menu()
                                            MDTextFieldHintText:
                                                id: hint_payment_type
                                                text: "Тип платежа"

                                    MDButton:
                                        style: "filled"
                                        size_hint_x: 1
                                        size_hint_y: None
                                        height: dp(48)
                                        on_release: app.calculate()
                                        MDButtonText:
                                            id: btn_calculate_text
                                            text: "Рассчитать"

                                    MDLabel:
                                        id: label_results_title
                                        text: "Результаты расчёта"
                                        adaptive_height: True
                                        bold: True

                                    MDLabel:
                                        id: label_result_monthly
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_interest
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_total
                                        adaptive_height: True
                                        text: "—"

                                    MDLabel:
                                        id: label_result_effective
                                        adaptive_height: True
                                        text: "—"

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(8)
                                padding: dp(12)
                                size_hint: 1, 1

                                MDLabel:
                                    id: label_table_title
                                    text: "Таблица — график платежей"
                                    adaptive_height: True
                                    bold: True

                                MDScrollView:
                                    do_scroll_x: False
                                    bar_width: dp(6)
                                    size_hint: 1, 1

                                    MDList:
                                        id: schedule_list
                                        size_hint_y: None
                                        height: self.minimum_height

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(6)
                                padding: dp(8)
                                size_hint: 1, 1

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(6)
                                    id: graph_header_band
                                    md_bg_color: 0.93, 0.94, 0.96, 1

                                    MDLabel:
                                        id: graph_title_lbl
                                        text: "График платежей"
                                        halign: "center"
                                        adaptive_height: True
                                        bold: True

                                    MDLabel:
                                        id: graph_subtitle_lbl
                                        text: "Столбцы: проценты (красный) и основные платежа (синий) по месяцам"
                                        halign: "center"
                                        adaptive_height: True
                                        font_style: "Body"
                                        role: "small"
                                        theme_text_color: "Secondary"

                                MDBoxLayout:
                                    orientation: "horizontal"
                                    spacing: dp(16)
                                    padding: dp(8), dp(4)
                                    size_hint_y: None
                                    height: dp(40)
                                    id: graph_legend_band
                                    md_bg_color: 0.94, 0.95, 0.97, 1

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(4)
                                        size_hint_x: 0.5
                                        CheckBox:
                                            id: graph_cb_interest
                                            size_hint: None, None
                                            size: dp(32), dp(32)
                                            active: True
                                            on_active: app.redraw_charts_only()
                                        MDLabel:
                                            id: graph_legend_interest_lbl
                                            text: "Проценты"
                                            valign: "middle"

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(4)
                                        size_hint_x: 0.5
                                        CheckBox:
                                            id: graph_cb_principal
                                            size_hint: None, None
                                            size: dp(32), dp(32)
                                            active: True
                                            on_active: app.redraw_charts_only()
                                        MDLabel:
                                            id: graph_legend_principal_lbl
                                            text: "Основной"
                                            valign: "middle"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: dp(4)
                                    padding: dp(6)
                                    size_hint: 1, 1
                                    id: graph_plot_band
                                    md_bg_color: 0.98, 0.99, 1.0, 1

                                    Widget:
                                        id: graph
                                        size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(6)
                                padding: dp(8)
                                size_hint: 1, 1

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height
                                    padding: dp(6)
                                    id: chart_header_band
                                    md_bg_color: 0.93, 0.94, 0.96, 1

                                    MDLabel:
                                        id: chart_title_lbl
                                        text: "Совокупные выплаты"
                                        halign: "center"
                                        adaptive_height: True
                                        bold: True

                                    MDLabel:
                                        id: chart_subtitle_lbl
                                        text: "Круговая диаграмма: доля процентов и основной в общей сумме выплат"
                                        halign: "center"
                                        adaptive_height: True
                                        font_style: "Body"
                                        role: "small"
                                        theme_text_color: "Secondary"

                                MDBoxLayout:
                                    orientation: "horizontal"
                                    spacing: dp(16)
                                    padding: dp(8), dp(4)
                                    size_hint_y: None
                                    height: dp(40)
                                    id: chart_legend_band
                                    md_bg_color: 0.94, 0.95, 0.97, 1

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(4)
                                        size_hint_x: 0.5
                                        CheckBox:
                                            id: chart_cb_interest
                                            size_hint: None, None
                                            size: dp(32), dp(32)
                                            active: True
                                            on_active: app.redraw_charts_only()
                                        MDLabel:
                                            id: chart_legend_interest_lbl
                                            text: "Проценты"
                                            valign: "middle"

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: dp(4)
                                        size_hint_x: 0.5
                                        CheckBox:
                                            id: chart_cb_principal
                                            size_hint: None, None
                                            size: dp(32), dp(32)
                                            active: True
                                            on_active: app.redraw_charts_only()
                                        MDLabel:
                                            id: chart_legend_principal_lbl
                                            text: "Основной"
                                            valign: "middle"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: dp(4)
                                    padding: dp(6)
                                    size_hint: 1, 1
                                    id: chart_plot_band
                                    md_bg_color: 0.98, 0.99, 1.0, 1

                                    Widget:
                                        id: chart
                                        size_hint: 1, 1

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: dp(12)
                                padding: dp(16)
                                size_hint: 1, 1

                                MDLabel:
                                    id: sum_title_lbl
                                    text: "Сводка по кредиту"
                                    adaptive_height: True
                                    bold: True

                                MDLabel:
                                    id: sum_subtitle_lbl
                                    text: "Данные после нажатия «Рассчитать» на вкладке «Ввод»."
                                    adaptive_height: True
                                    font_style: "Body"
                                    role: "small"
                                    theme_text_color: "Secondary"

                                MDLabel:
                                    id: sum_content
                                    text: "Нет данных — выполните расчёт на вкладке «Ввод»."
                                    size_hint_y: 1
                                    valign: "top"
                                    halign: "left"
                                    text_size: self.width, None

        MDNavigationDrawer:
            id: nav_drawer
            drawer_type: "modal"
            radius: (0, dp(16), dp(16), 0)

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    orientation: "vertical"
                    padding: 0, 0, 0, "12dp"
                    adaptive_height: True

                    MDLabel:
                        id: nav_hdr_title
                        text: "Калькулятор ипотеки"
                        adaptive_height: True
                        padding: "16dp", 0, "16dp", 0
                        font_style: "Display"
                        role: "small"

                    MDLabel:
                        id: nav_hdr_sub
                        text: "Меню навигации"
                        adaptive_height: True
                        padding: "18dp", 0, "18dp", 0
                        font_style: "Title"
                        role: "large"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    id: nav_lbl_sections
                    text: "Разделы"

                MDNavigationDrawerItem:
                    on_release: app.go_tab_input()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "calculator"
                    MDNavigationDrawerItemText:
                        id: nav_item_calc_text
                        text: "Расчёт ипотеки"

                MDNavigationDrawerItem:
                    on_release: app.go_tab_charts()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "chart-line"
                    MDNavigationDrawerItemText:
                        id: nav_item_charts_text
                        text: "Графики и диаграммы"

                MDNavigationDrawerItem:
                    on_release: app.open_repository()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "github"
                    MDNavigationDrawerItemText:
                        id: nav_item_source_text
                        text: "Исходный код"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    id: nav_lbl_appearance
                    text: "Оформление"

                MDNavigationDrawerItem:
                    on_release: app.set_theme_light()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "weather-sunny"
                    MDNavigationDrawerItemText:
                        id: nav_item_theme_light_text
                        text: "Светлая тема"

                MDNavigationDrawerItem:
                    on_release: app.set_theme_dark()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "weather-night"
                    MDNavigationDrawerItemText:
                        id: nav_item_theme_dark_text
                        text: "Тёмная тема"

                MDNavigationDrawerLabel:
                    id: nav_lbl_language
                    text: "Язык"

                MDNavigationDrawerItem:
                    on_release: app.set_lang_ru()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "translate"
                    MDNavigationDrawerItemText:
                        id: nav_item_lang_ru_text
                        text: "Русский"

                MDNavigationDrawerItem:
                    on_release: app.set_lang_en()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "translate-variant"
                    MDNavigationDrawerItemText:
                        id: nav_item_lang_en_text
                        text: "English"

                MDNavigationDrawerDivider:

                MDNavigationDrawerLabel:
                    id: nav_lbl_extra
                    text: "Дополнительно"

                MDNavigationDrawerItem:
                    on_release: app.open_about()
                    MDNavigationDrawerItemLeadingIcon:
                        icon: "information-outline"
                    MDNavigationDrawerItemText:
                        id: nav_item_about_text
                        text: "О приложении"

        MDTopAppBar:
            id: top_bar
            type: "small"
            pos_hint: {"top": 1}

            MDTopAppBarLeadingButtonContainer:

                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: root.ids.nav_drawer.set_state("toggle")

            MDTopAppBarTitle:
                id: top_bar_title
                text: "Mortgage Calculator"

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "star"
                    on_release: app.open_repository()
"""


class MortgageCalculatorApp(MDApp):
    payment_type_menu: MDDropdownMenu | None = None
    about_dialog: MDDialog | None = None
    _plot_canvas_bound: bool = False
    _last_schedule_rows: list | None = None
    lang: str = "ru"

    def tr(self, key: str, **kwargs) -> str:
        table = STRINGS.get(self.lang) or STRINGS["ru"]
        s = table.get(key, key)
        return s.format(**kwargs) if kwargs else s

    def _prefs_path(self) -> str:
        return os.path.join(self.user_data_dir, PREFS_FILENAME)

    def _load_prefs(self) -> None:
        self.lang = "ru"
        self.theme_cls.theme_style = "Light"
        try:
            path = self._prefs_path()
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                lang = data.get("lang", "ru")
                if lang in STRINGS:
                    self.lang = lang
                theme = data.get("theme", "Light")
                if theme in ("Light", "Dark"):
                    self.theme_cls.theme_style = theme
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            pass

    def _save_prefs(self) -> None:
        try:
            path = self._prefs_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    {"lang": self.lang, "theme": self.theme_cls.theme_style},
                    f,
                    ensure_ascii=False,
                )
        except OSError:
            pass

    def _close_nav_drawer(self) -> None:
        drawer = self.root.ids.get("nav_drawer") if getattr(self, "root", None) else None
        if drawer is not None:
            drawer.set_state("close")

    def set_theme_light(self, *args) -> None:
        self.theme_cls.theme_style = "Light"
        self._save_prefs()
        self._apply_theme_colors()
        self._draw_graph_background(self.root.ids.graph)
        self._draw_graph_background(self.root.ids.chart)
        if self._last_schedule_rows:
            self._draw_graph_bars(self.root.ids.graph, self._last_schedule_rows)
            self._draw_pie_chart(self.root.ids.chart, self._last_schedule_rows)
        self._close_nav_drawer()

    def set_theme_dark(self, *args) -> None:
        self.theme_cls.theme_style = "Dark"
        self._save_prefs()
        self._apply_theme_colors()
        self._draw_graph_background(self.root.ids.graph)
        self._draw_graph_background(self.root.ids.chart)
        if self._last_schedule_rows:
            self._draw_graph_bars(self.root.ids.graph, self._last_schedule_rows)
            self._draw_pie_chart(self.root.ids.chart, self._last_schedule_rows)
        self._close_nav_drawer()

    def set_lang_ru(self, *args) -> None:
        self.lang = "ru"
        self._save_prefs()
        self._after_lang_change()

    def set_lang_en(self, *args) -> None:
        self.lang = "en"
        self._save_prefs()
        self._after_lang_change()

    def _after_lang_change(self) -> None:
        self._apply_i18n()
        self._sync_payment_type_text_to_lang()
        self._setup_payment_type_dropdown()
        self._rebuild_schedule_from_cache()
        self._close_nav_drawer()

    def _sync_payment_type_text_to_lang(self) -> None:
        if not getattr(self, "root", None):
            return
        field = self.root.ids.field_payment_type
        field.text = self.tr("pay_diff") if payment_type_is_diff(field.text) else self.tr("pay_annuity")

    def _rebuild_schedule_from_cache(self) -> None:
        """Rebuild table and charts from last inputs if schedule was computed."""
        if not getattr(self, "root", None):
            return
        self.calculate()

    def _apply_i18n(self) -> None:
        if not getattr(self, "root", None):
            return
        ids = self.root.ids
        mapping = [
            ("tab_text_input", "tab_input"),
            ("tab_text_table", "tab_table"),
            ("tab_text_graph", "tab_graph"),
            ("tab_text_chart", "tab_chart"),
            ("tab_text_sum", "tab_sum"),
            ("nav_hdr_title", "nav_app"),
            ("nav_hdr_sub", "nav_menu"),
            ("nav_lbl_sections", "nav_sections"),
            ("nav_item_calc_text", "nav_calc"),
            ("nav_item_charts_text", "nav_charts"),
            ("nav_item_source_text", "nav_source"),
            ("nav_lbl_extra", "nav_extra"),
            ("nav_item_about_text", "nav_about"),
            ("nav_lbl_appearance", "nav_appearance"),
            ("nav_item_theme_light_text", "nav_theme_light"),
            ("nav_item_theme_dark_text", "nav_theme_dark"),
            ("nav_lbl_language", "nav_language"),
            ("nav_item_lang_ru_text", "nav_lang_ru"),
            ("nav_item_lang_en_text", "nav_lang_en"),
            ("label_params_title", "params_title"),
            ("label_results_title", "results_title"),
            ("label_table_title", "table_title"),
            ("graph_title_lbl", "graph_title"),
            ("graph_subtitle_lbl", "graph_subtitle"),
            ("graph_legend_interest_lbl", "legend_interest"),
            ("graph_legend_principal_lbl", "legend_principal"),
            ("chart_title_lbl", "chart_title"),
            ("chart_subtitle_lbl", "chart_subtitle"),
            ("chart_legend_interest_lbl", "legend_interest"),
            ("chart_legend_principal_lbl", "legend_principal"),
            ("sum_title_lbl", "sum_title"),
            ("sum_subtitle_lbl", "sum_subtitle"),
            ("top_bar_title", "app_title"),
            ("btn_calculate_text", "btn_calculate"),
        ]
        for wid, key in mapping:
            w = ids.get(wid)
            if w is not None:
                w.text = self.tr(key)
        for hint_id, key in (
            ("hint_start_date", "hint_start_date"),
            ("hint_property_price", "hint_property_price"),
            ("hint_term_years", "hint_term_years"),
            ("hint_loan_amount", "hint_loan_amount"),
            ("hint_down_payment", "hint_down_payment"),
            ("hint_rate", "hint_rate"),
            ("hint_payment_type", "hint_payment_type"),
        ):
            h = ids.get(hint_id)
            if h is not None:
                h.text = self.tr(key)
        if not self._last_schedule_rows:
            self._fill_sum_tab_empty()

    def _apply_theme_colors(self) -> None:
        if not getattr(self, "root", None):
            return
        ids = self.root.ids
        dark_bg = getattr(self.theme_cls, "bg_darkest", None) or getattr(
            self.theme_cls, "bg_dark", [0.12, 0.12, 0.12, 1]
        )
        ids.main_tabs.md_bg_color = dark_bg
        ids.top_bar.md_bg_color = dark_bg
        dark = self.theme_cls.theme_style == "Dark"
        if dark:
            ids.tab_carousel.md_bg_color = getattr(self.theme_cls, "bg_dark", (0.11, 0.11, 0.12, 1))
            band1 = (0.18, 0.19, 0.22, 1)
            band2 = (0.2, 0.21, 0.24, 1)
            plot_bg = (0.14, 0.15, 0.17, 1)
        else:
            ids.tab_carousel.md_bg_color = "#FFFFFF"
            band1 = (0.93, 0.94, 0.96, 1)
            band2 = (0.94, 0.95, 0.97, 1)
            plot_bg = (0.98, 0.99, 1.0, 1)
        for k in (
            "graph_header_band",
            "chart_header_band",
        ):
            w = ids.get(k)
            if w is not None:
                w.md_bg_color = band1
        for k in ("graph_legend_band", "chart_legend_band"):
            w = ids.get(k)
            if w is not None:
                w.md_bg_color = band2
        for k in ("graph_plot_band", "chart_plot_band"):
            w = ids.get(k)
            if w is not None:
                w.md_bg_color = plot_bg

    def open_about(self, *args) -> None:
        self._close_nav_drawer()
        if self.about_dialog is not None:
            try:
                self.about_dialog.dismiss()
            except Exception:
                pass
            self.about_dialog = None

        def on_ok(*_a) -> None:
            if self.about_dialog is not None:
                self.about_dialog.dismiss()
            self.about_dialog = None

        dlg = MDDialog(
            MDDialogHeadlineText(text=self.tr("about_title"), halign="left"),
            MDDialogSupportingText(text=self.tr("about_body"), halign="left"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text=self.tr("about_ok")),
                    style="text",
                    on_release=on_ok,
                ),
                spacing="8dp",
            ),
        )
        self.about_dialog = dlg
        dlg.open()

    def _fill_sum_tab(
        self,
        *,
        principal: float,
        n_months: int,
        years_f: float,
        annual: float,
        is_diff: bool,
        interest: float,
        total: float,
        eff: float,
        first_m: float | None,
        last_m: float | None,
        monthly: float | None,
    ) -> None:
        ids = self.root.ids
        sc = ids.get("sum_content")
        if sc is None:
            return
        pay_label = self.tr("pay_diff") if is_diff else self.tr("pay_annuity")
        if is_diff and first_m is not None and last_m is not None:
            pay_line = self.tr("sum_monthly", v=f"{_fmt_rub(first_m)} → {_fmt_rub(last_m)}")
        elif monthly is not None:
            pay_line = self.tr("sum_monthly", v=_fmt_rub(monthly))
        else:
            pay_line = self.tr("sum_monthly", v=self.tr("dash"))
        y_str = f"{years_f:g}"
        lines = [
            self.tr("sum_principal", v=_fmt_rub(principal)),
            self.tr("sum_term", months=n_months, years=y_str),
            self.tr("sum_rate", pct=_fmt_pct(annual)),
            self.tr("sum_type", t=pay_label),
            pay_line,
            self.tr("sum_interest", v=_fmt_rub(interest)),
            self.tr("sum_total", v=_fmt_rub(total)),
            self.tr("sum_eff", pct=_fmt_pct(eff)),
        ]
        sc.text = "\n".join(lines)

    def _fill_sum_tab_empty(self) -> None:
        sc = self.root.ids.get("sum_content") if getattr(self, "root", None) else None
        if sc is not None:
            sc.text = self.tr("sum_empty")

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self._load_prefs()
        return Builder.load_string(KV)

    def _on_tabs_switch(self, tabs: MDTabsPrimary, tab_item, tab_content) -> None:
        """Triggered every time the current tab is changed."""
        tab_title = None
        try:
            if tab_item is not None and hasattr(tab_item, "walk"):
                for w in tab_item.walk():
                    if isinstance(w, MDTabsItemText):
                        tab_title = w.text
                        break
        except Exception:
            tab_title = None

        # Keep logs in English (required).
        print(f"Tab switched: {tab_title}")

    def on_start(self) -> None:
        tabs: MDTabsPrimary = self.root.ids.main_tabs

        tabs.bind(on_tab_switch=self._on_tabs_switch)

        self._apply_theme_colors()

        tabs.switch_tab(icon="view-grid-outline")

        self._apply_i18n()
        self._setup_payment_type_dropdown()
        self._apply_default_form_values()
        # Lesson: run same calculation as the button so the screen shows numbers on launch.
        Clock.schedule_once(lambda _dt: self.calculate(), 0.15)
        # Draw plot frames so Graph/Chart tabs are not blank before first interaction.
        Clock.schedule_once(lambda _dt: self._prime_empty_plots(), 0.22)

    def _prime_empty_plots(self) -> None:
        self._ensure_plot_canvas_bindings()
        self._draw_graph_background(self.root.ids.graph)
        self._draw_graph_background(self.root.ids.chart)

    def _ensure_plot_canvas_bindings(self) -> None:
        """Bind graph/chart Widget once so canvas.before tracks size (lesson: draw_graph area)."""
        if self._plot_canvas_bound:
            return
        self._plot_canvas_bound = True
        for key in ("graph", "chart"):
            w = self.root.ids[key]
            w.bind(pos=self._on_plot_widget_layout, size=self._on_plot_widget_layout)
        print("Plot canvas bindings attached (graph, chart)")

    def _on_plot_widget_layout(self, instance, *args) -> None:
        """Resize: redraw plot frame + chart layers (lesson: graph rebuild on layout)."""
        self._draw_graph_background(self.root.ids.graph)
        self._draw_graph_background(self.root.ids.chart)
        if self._last_schedule_rows:
            self._draw_graph_bars(self.root.ids.graph, self._last_schedule_rows)
            self._draw_pie_chart(self.root.ids.chart, self._last_schedule_rows)

    def _draw_graph_background(self, w) -> None:
        """Fill plot area and draw border (Kivy graphics: Color, Rectangle, Line)."""
        w.canvas.before.clear()
        if self.theme_cls.theme_style == "Dark":
            fill = (0.16, 0.17, 0.2, 1)
            border = (0.5, 0.55, 0.65, 1)
        else:
            fill = (0.92, 0.94, 0.98, 1)
            border = (0.45, 0.5, 0.58, 1)
        with w.canvas.before:
            Color(*fill)
            Rectangle(pos=w.pos, size=w.size)
            Color(*border)
            Line(rectangle=(w.x, w.y, w.width, w.height), width=dp(1.5))

    def redraw_charts_only(self, *args) -> None:
        """Checkbox toggled: repaint bars and pie from cached schedule (no full recalculate)."""
        Clock.schedule_once(lambda _dt: self._paint_both_charts_once(), 0.02)

    def _paint_both_charts_once(self) -> None:
        if not getattr(self, "root", None):
            return
        g = self.root.ids.graph
        c = self.root.ids.chart
        self._draw_graph_background(g)
        self._draw_graph_background(c)
        if self._last_schedule_rows:
            self._draw_graph_bars(g, self._last_schedule_rows)
            self._draw_pie_chart(c, self._last_schedule_rows)

    def _draw_graph_bars(self, w, rows: list) -> None:
        """Stacked bar chart: blue = principal part, red = interest (lesson-style loop on canvas)."""
        w.canvas.clear()
        if not rows or w.width < dp(24):
            return
        ids = self.root.ids
        show_i = ids.graph_cb_interest.active
        show_p = ids.graph_cb_principal.active
        pad = dp(14)
        max_stack = max((r[3] + r[4]) for r in rows) or 1.0
        plot_h = max(w.height - 2 * pad, dp(1))
        plot_w = max(w.width - 2 * pad, dp(1))
        n = len(rows)
        gap = dp(1.5)
        bar_w = max((plot_w - gap * max(n - 1, 0)) / max(n, 1), dp(2))
        base_x = w.x + pad
        base_y = w.y + pad
        with w.canvas:
            for i, row in enumerate(rows):
                intr, prin = row[3], row[4]
                bh_p = plot_h * (prin / max_stack) if show_p else 0.0
                bh_i = plot_h * (intr / max_stack) if show_i else 0.0
                bx = base_x + i * (bar_w + gap)
                y0 = base_y
                if show_p and bh_p > 0:
                    Color(0.15, 0.35, 0.92, 1)
                    Rectangle(pos=(bx, y0), size=(bar_w, bh_p))
                    y0 += bh_p
                if show_i and bh_i > 0:
                    Color(0.92, 0.18, 0.2, 1)
                    Rectangle(pos=(bx, y0), size=(bar_w, bh_i))

    def _draw_pie_chart(self, w, rows: list) -> None:
        """Two-sector pie: total interest vs total principal paid (Ellipse, angle_start / angle_end)."""
        w.canvas.clear()
        if not rows or w.width < dp(24):
            return
        ids = self.root.ids
        show_i = ids.chart_cb_interest.active
        show_p = ids.chart_cb_principal.active
        t_int = sum(r[3] for r in rows) if show_i else 0.0
        t_prin = sum(r[4] for r in rows) if show_p else 0.0
        total = t_int + t_prin
        if total <= 1e-9:
            return
        cx = w.center_x
        cy = w.center_y
        rad = 0.38 * min(w.width, w.height)
        a_int = 360.0 * (t_int / total)
        with w.canvas:
            if t_int > 1e-6 and show_i:
                Color(0.92, 0.2, 0.22, 1)
                Ellipse(
                    pos=(cx - rad, cy - rad),
                    size=(2 * rad, 2 * rad),
                    angle_start=0.0,
                    angle_end=a_int,
                )
            if t_prin > 1e-6 and show_p:
                Color(0.18, 0.42, 0.88, 1)
                Ellipse(
                    pos=(cx - rad, cy - rad),
                    size=(2 * rad, 2 * rad),
                    angle_start=a_int,
                    angle_end=360.0,
                )

    def calculate(self, *args) -> None:
        """
        Read Input tab fields, compute mortgage summary (no input validation yet — lesson scope).
        Updates result labels; logs in English.
        """
        ids = self.root.ids
        start_d = _parse_start_date(ids.field_start_date.text)

        try:
            principal = float((ids.field_loan_amount.text or "0").replace(" ", "").replace(",", "."))
            years_f = float((ids.field_term_years.text or "0").replace(",", "."))
            n_months = max(0, int(round(years_f * 12)))
            annual = float((ids.field_rate.text or "0").replace(",", "."))
        except ValueError:
            self._last_schedule_rows = None
            ids.schedule_list.clear_widgets()
            for key in ("graph", "chart"):
                w = ids[key]
                w.canvas.before.clear()
                w.canvas.clear()
            ids.label_result_monthly.text = self.tr("err_numeric")
            ids.label_result_interest.text = self.tr("dash")
            ids.label_result_total.text = self.tr("dash")
            ids.label_result_effective.text = self.tr("dash")
            self._fill_sum_tab_empty()
            print("Calculate failed: invalid numeric input")
            return
        pay_type = (ids.field_payment_type.text or "").strip()

        if start_d:
            print(f"Calculate using start date: {start_d.isoformat()}")
        else:
            print("Calculate: start date not parsed, continuing with loan math only")

        eff = _effective_annual_percent(annual)
        is_diff = payment_type_is_diff(pay_type)

        if n_months <= 0 or principal <= 0:
            self._last_schedule_rows = None
            ids.schedule_list.clear_widgets()
            for key in ("graph", "chart"):
                w = ids[key]
                w.canvas.before.clear()
                w.canvas.clear()
            ids.label_result_monthly.text = self.tr("res_payment_none")
            ids.label_result_interest.text = self.tr("res_interest_none")
            ids.label_result_total.text = self.tr("res_total_none")
            ids.label_result_effective.text = self.tr("res_eff", pct=_fmt_pct(eff))
            self._fill_sum_tab_empty()
            print("Calculate skipped: invalid principal or term")
            return

        first_m = last_m = None
        monthly = None
        if is_diff:
            first_m, last_m, interest, total = _totals_differentiated(principal, annual, n_months)
            ids.label_result_monthly.text = self.tr(
                "res_monthly_diff", first=_fmt_rub(first_m), last=_fmt_rub(last_m)
            )
        else:
            monthly, interest, total = _totals_annuity(principal, annual, n_months)
            ids.label_result_monthly.text = self.tr("res_monthly_annuity", amt=_fmt_rub(monthly))

        ids.label_result_interest.text = self.tr("sum_interest", v=_fmt_rub(interest))
        ids.label_result_total.text = self.tr("sum_total", v=_fmt_rub(total))
        ids.label_result_effective.text = self.tr("sum_eff", pct=_fmt_pct(eff))

        self._rebuild_schedule_list(principal, annual, n_months, is_diff, start_d)

        self._fill_sum_tab(
            principal=principal,
            n_months=n_months,
            years_f=years_f,
            annual=annual,
            is_diff=is_diff,
            interest=interest,
            total=total,
            eff=eff,
            first_m=first_m,
            last_m=last_m,
            monthly=monthly,
        )

        Clock.schedule_once(lambda _dt: self._paint_both_charts_once(), 0.05)

        print(
            f"Calculate done: differentiated={is_diff}, principal={principal}, months={n_months}, "
            f"interest={interest:.2f}, total={total:.2f}"
        )

    def _rebuild_schedule_list(
        self,
        principal: float,
        annual: float,
        n_months: int,
        is_diff: bool,
        start_d: date | None,
    ) -> None:
        """Fill MDList on Table tab: header + one row per month (lesson: zebra striping)."""
        lst = self.root.ids.schedule_list
        lst.clear_widgets()

        base = start_d or date.today()
        if is_diff:
            rows = _schedule_differentiated_rows(principal, annual, n_months, base)
        else:
            rows = _schedule_annuity_rows(principal, annual, n_months, base)

        dark = self.theme_cls.theme_style == "Dark"
        if dark:
            header_bg = (0.22, 0.24, 0.28, 1.0)
            row_a = (0.16, 0.17, 0.19, 1.0)
            row_b = (0.2, 0.21, 0.23, 1.0)
        else:
            header_bg = (0.86, 0.89, 0.93, 1.0)
            row_a = (1.0, 1.0, 1.0, 1.0)
            row_b = (0.9, 0.91, 0.94, 1.0)

        header_texts = (
            self.tr("col_no"),
            self.tr("col_date"),
            self.tr("col_payment"),
            self.tr("col_interest"),
            self.tr("col_principal"),
            self.tr("col_balance"),
        )
        lst.add_widget(_schedule_table_row_widget(header_texts, header_bg, header=True))

        for month_no, pay_date, payment, interest, principal_part, balance_after in rows:
            bg = row_a if month_no % 2 == 1 else row_b
            texts = (
                str(month_no),
                pay_date.strftime("%d.%m.%Y"),
                _fmt_rub(payment),
                _fmt_rub(interest),
                _fmt_rub(principal_part),
                _fmt_rub(balance_after),
            )
            lst.add_widget(_schedule_table_row_widget(texts, bg))

        self._last_schedule_rows = rows
        print(f"Payment table rebuilt: {len(rows)} data rows")

    def _apply_default_form_values(self) -> None:
        """Lesson defaults: sample loan params + today's date in the start date field."""
        ids = self.root.ids
        ids.field_start_date.text = date.today().strftime("%d.%m.%Y")
        ids.field_property_price.text = "5000000"
        ids.field_term_years.text = "10"
        ids.field_loan_amount.text = "5000000"
        ids.field_down_payment.text = "0"
        ids.field_rate.text = "9.5"
        ids.field_payment_type.text = self.tr("pay_annuity")

    def open_start_date_picker(self, *args) -> None:
        """Open modal date picker (KivyMD 2: MDModalDatePicker; KivyMD 1.x: MDDatePicker)."""
        field = self.root.ids.field_start_date
        picker_date = date.today()
        raw = (field.text or "").strip().replace("/", ".")
        if raw:
            parts = raw.split(".")
            if len(parts) == 3:
                try:
                    d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                    picker_date = date(y, m, d)
                except (ValueError, OverflowError):
                    pass
        if MDModalDatePicker is not None:
            dlg = MDModalDatePicker(
                year=picker_date.year,
                month=picker_date.month,
                day=picker_date.day,
            )
            dlg.bind(on_ok=self._on_start_date_ok, on_cancel=self._on_start_date_cancel)
            dlg.open()
        else:
            assert MDDatePicker is not None
            dlg = MDDatePicker(
                year=picker_date.year,
                month=picker_date.month,
                day=picker_date.day,
            )
            dlg.bind(on_save=self._on_start_date_save_v1, on_cancel=self._on_start_date_cancel_v1)
            dlg.open()

    def _on_start_date_ok(self, picker_instance) -> None:
        chosen = picker_instance.get_date()[0]
        field = self.root.ids.field_start_date
        field.text = chosen.strftime("%d.%m.%Y")
        field.focus = False
        print(f"Start date selected: {chosen.isoformat()}")

    def _on_start_date_cancel(self, picker_instance) -> None:
        self.root.ids.field_start_date.focus = False
        print("Start date picker cancelled")

    def _on_start_date_save_v1(self, instance, value, date_range) -> None:
        if value is None:
            return
        field = self.root.ids.field_start_date
        field.text = value.strftime("%d.%m.%Y")
        field.focus = False
        print(f"Start date selected: {value.isoformat()}")

    def _on_start_date_cancel_v1(self, instance, value) -> None:
        self.root.ids.field_start_date.focus = False
        print("Start date picker cancelled")

    def _setup_payment_type_dropdown(self) -> None:
        """Bind MDDropdownMenu to payment type field (lesson: annuity vs differentiated)."""
        field = self.root.ids.field_payment_type
        label_a = self.tr("pay_annuity")
        label_d = self.tr("pay_diff")
        menu_items = [
            {
                "text": label_a,
                "leading_icon": "chart-timeline-variant",
                "on_release": lambda *a, t=label_a: self._on_payment_type_chosen(t),
            },
            {
                "text": label_d,
                "leading_icon": "chart-line-variant",
                "on_release": lambda *a, t=label_d: self._on_payment_type_chosen(t),
            },
        ]
        self.payment_type_menu = MDDropdownMenu(
            caller=field,
            items=menu_items,
            position="bottom",
            width_mult=5,
        )

    def open_payment_type_menu(self, *args) -> None:
        """KV calls this when the payment type field gains focus."""
        if self.payment_type_menu:
            self.payment_type_menu.open()

    def _on_payment_type_chosen(self, label: str) -> None:
        """Write selected menu text into the field and close menu (lesson pattern)."""
        if self.payment_type_menu:
            self.payment_type_menu.dismiss()

        def apply_choice(_dt):
            field = self.root.ids.field_payment_type
            field.text = label
            field.focus = False

        # Small delay so dismiss finishes before updating text (similar to lesson Clock.schedule_once).
        Clock.schedule_once(apply_choice, 0.05)

    def go_tab_input(self, *args) -> None:
        """Drawer: switch to the Input tab (loan calculation form)."""
        self._close_nav_drawer()
        if getattr(self, "root", None):
            self.root.ids.main_tabs.switch_tab(icon="view-grid-outline")

    def go_tab_charts(self, *args) -> None:
        """Drawer: switch to the Graph tab (bar chart; use tabs for pie chart)."""
        self._close_nav_drawer()
        if getattr(self, "root", None):
            self.root.ids.main_tabs.switch_tab(icon="chart-line")

    def open_repository(self, *args) -> None:
        drawer = self.root.ids.get("nav_drawer")
        if drawer is not None:
            drawer.set_state("close")
        webbrowser.open(SOURCE_CODE_URL)


# If dropdown menus misbehave on some KivyMD builds, pin a known-good version, e.g.:
#   pip install "kivy>=2.3,<3" "kivymd>=2.0.0" --upgrade
# On Android, soft keyboard + overlays sometimes need: Window.softinput_mode (see Kivy docs).


MortgageCalculatorApp().run()
