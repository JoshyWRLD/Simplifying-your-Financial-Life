from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class SimplifyingYourFinancialLifeApp(App):
    def build(self):
        self.icon = "Simplifying 2.png"
        # Set the window size and background color
        Window.size = (400, 700)
        Window.clearcolor = (1, 1, 0, 1)  # Set background color to white

        # Create a screen manager
        self.sm = ScreenManager()

        # Create the main screen
        main_screen = MainScreen(name='main')
        self.sm.add_widget(main_screen)

        return self.sm


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.summary_hidden = True  # Initially hide the summary

        # Create a BoxLayout with a vertical orientation
        layout = BoxLayout(orientation='vertical')

        # Create labels and entry fields for income
        layout.add_widget(self.create_label("Income Source:"))
        self.income_source_entry = self.create_entry()
        layout.add_widget(self.income_source_entry)
        layout.add_widget(self.create_label("Amount (₱):"))
        self.income_amount_entry = self.create_entry()
        layout.add_widget(self.income_amount_entry)
        layout.add_widget(self.create_button("Add Income", self.add_income))

        # Create labels and entry fields for expenses
        layout.add_widget(self.create_label("Expense Category:"))
        self.expense_category_entry = self.create_entry()
        layout.add_widget(self.expense_category_entry)
        layout.add_widget(self.create_label("Amount (₱):"))
        self.expense_amount_entry = self.create_entry()
        layout.add_widget(self.expense_amount_entry)
        layout.add_widget(self.create_button("Add Expense", self.add_expense))

        # Create labels and entry fields for savings
        layout.add_widget(self.create_label("Savings Goal (₱):"))
        self.savings_goal_entry = self.create_entry()
        layout.add_widget(self.savings_goal_entry)
        layout.add_widget(self.create_button("Set Savings Goal", self.set_savings_goal))

        layout.add_widget(self.create_label("Add to Savings (₱):"))
        self.add_to_savings_entry = self.create_entry()
        layout.add_widget(self.add_to_savings_entry)
        layout.add_widget(self.create_button("Add to Savings", self.add_to_savings))

        layout.add_widget(self.create_button("Summary", self.toggle_summary))

        self.income = []
        self.expenses = []
        self.savings_goal = 0
        self.savings_balance = 0

        self.summary_text = TextInput(height=200, readonly=True, multiline=True)
        self.summary_scrollview = ScrollView(size_hint=(1, None), height=0)
        self.summary_scrollview.add_widget(self.summary_text)

        layout.add_widget(self.summary_scrollview)

        self.add_widget(layout)

        self.popup = None  # Initialize a popup

    def create_label(self, text):
        label = Label(text=text, color=(0.2, 0.2, 0.2, 1))  # Set label text color
        return label

    def create_entry(self):
        entry = TextInput(multiline=False, background_color=(0.95, 0.95, 0.95, 1))  # Set entry background color
        entry.bind(text=self.on_entry_text_change)
        return entry

    def create_button(self, text, on_release):
        button = Button(text=text, background_color=(0.2, 0.5, 0.8, 1))  # Set button background color
        button.bind(on_release=on_release)
        return button

    def add_income(self, instance):
        source = self.income_source_entry.text
        amount_text = self.income_amount_entry.text
        if not amount_text:
            self.show_warning("Amount is required")
            return

        try:
            amount = float(amount_text)
            self.income.append({"source": source, "amount": amount})
            self.update_summary()
            self.clear_entries(self.income_source_entry, self.income_amount_entry)
        except ValueError:
            self.show_warning("Invalid Amount")

    def add_expense(self, instance):
        category = self.expense_category_entry.text
        amount_text = self.expense_amount_entry.text
        if not amount_text:
            self.show_warning("Amount is required")
            return

        try:
            amount = float(amount_text)
            self.expenses.append({"category": category, "amount": amount})
            self.update_summary()
            self.clear_entries(self.expense_category_entry, self.expense_amount_entry)
        except ValueError:
            self.show_warning("Invalid Amount")

    def set_savings_goal(self, instance):
        goal_text = self.savings_goal_entry.text
        if not goal_text:
            self.show_warning("Savings Goal is required")
            return

        try:
            goal = float(goal_text)
            self.savings_goal = goal
            self.update_summary()
            self.clear_entries(self.savings_goal_entry)
        except ValueError:
            self.show_warning("Invalid Savings Goal")

    def add_to_savings(self, instance):
        amount_text = self.add_to_savings_entry.text
        if not amount_text:
            self.show_warning("Amount is required")
            return

        try:
            amount = float(amount_text)
            self.savings_balance += amount
            self.update_summary()
            self.clear_entries(self.add_to_savings_entry)
        except ValueError:
            self.show_warning("Invalid Amount")

    def toggle_summary(self, instance):
        if self.summary_hidden:
            self.summary_scrollview.height = 200
            self.summary_scrollview.opacity = 1
            instance.text = "Hide Summary"
        else:
            self.summary_scrollview.height = 0
            self.summary_scrollview.opacity = 0
            instance.text = "Summary"
        self.summary_hidden = not self.summary_hidden

    def update_summary(self):
        total_income = sum(item["amount"] for item in self.income)
        total_expenses = sum(item["amount"] for item in self.expenses)
        savings_progress = (self.savings_balance / self.savings_goal) * 100 if self.savings_goal > 0 else 0

        summary = f"Total Income: ₱{total_income:.2f}\n"
        summary += f"Total Expenses: ₱{total_expenses:.2f}\n"
        summary += f"Savings Goal: ₱{self.savings_goal:.2f}\n"
        summary += f"Savings Balance: ₱{self.savings_balance:.2f}\n"
        summary += f"Savings Progress: {savings_progress:.2f}%\n"

        self.summary_text.text = summary

    def clear_entries(self, *entries):
        for entry in entries:
            entry.text = ""

    def on_entry_text_change(self, instance, value):
        # Automatically update summary when text in an entry changes
        self.update_summary()

    def show_warning(self, message):
        # Create and display a warning popup
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=message))
        close_button = Button(text="OK")
        content.add_widget(close_button)
        self.popup = Popup(title="Warning", content=content, size_hint=(None, None), size=(300, 200), auto_dismiss=True)
        close_button.bind(on_release=self.popup.dismiss)
        self.popup.open()


if __name__ == "__main__":
    SimplifyingYourFinancialLifeApp().run()
