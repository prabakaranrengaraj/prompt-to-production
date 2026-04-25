import tkinter as tk
from decimal import Decimal, InvalidOperation, getcontext

# Set sufficient precision for financial and class 10 calculations
getcontext().prec = 28

class CalculatorApp:
    """
    A basic deterministic calculator intended for Class 10th students.
    Features core arithmetic, percentages, toggle sign, and precision math.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Student Calculator")
        
        # Dimensions and responsiveness
        self.root.geometry("400x650")
        self.root.minsize(350, 550)
        
        # Design System Variables: Deep Dark with Pastel Colored Buttons
        self.colors = {
            "bg": "#121212",             # Deep dark background
            "display_bg": "#1A1A1A",     # Slightly lighter for display area
            "text_main": "#FFFFFF",      # Main text
            "text_ghost": "#888888",     # History text
            "btn_num_bg": "#CDB4DB",     # Pastel purple for numbers
            "btn_num_fg": "#121212",     # Dark text on light pastel
            "btn_op_bg": "#FFC8DD",      # Pastel pink for operators
            "btn_op_fg": "#121212",      
            "btn_eq_bg": "#BDE0FE",      # Pastel blue for equals
            "btn_eq_fg": "#121212",      
            "btn_func_bg": "#FFAFCC",    # Pastel dark pink for functions
            "btn_func_fg": "#121212",    
            "focus_ring": "#FFFFFF"      # Focus color for keyboard navigation
        }
        
        self.root.configure(bg=self.colors["bg"])
        
        # Typography: Inter (Google Font) fallback to modern sans-serifs
        self.font_main = ('Inter', 48, 'bold')
        self.font_ghost = ('Inter', 20, 'normal')
        self.font_btn = ('Inter', 22, 'bold')
        
        # State variables
        self.current_expr = ""
        self.history_expr = ""
        self.last_operation_was_eval = False
        self.error_state = False
        
        self._build_ui()
        self._bind_keys()
        
    def _build_ui(self):
        """Builds the layout using grid to ensure responsive centering."""
        # Main Grid Layout
        self.root.grid_rowconfigure(0, weight=1) # Display area
        self.root.grid_rowconfigure(1, weight=4) # Buttons area
        self.root.grid_columnconfigure(0, weight=1)
        
        # --- Display Area ---
        display_frame = tk.Frame(self.root, bg=self.colors["display_bg"], padx=25, pady=25)
        display_frame.grid(row=0, column=0, sticky="nsew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Ghost History Label
        self.lbl_history = tk.Label(
            display_frame, text="", 
            font=self.font_ghost, bg=self.colors["display_bg"], 
            fg=self.colors["text_ghost"], anchor="se"
        )
        self.lbl_history.grid(row=0, column=0, sticky="nsew")
        
        # Current Value Label
        self.lbl_current = tk.Label(
            display_frame, text="0", 
            font=self.font_main, bg=self.colors["display_bg"], 
            fg=self.colors["text_main"], anchor="e"
        )
        self.lbl_current.grid(row=1, column=0, sticky="nsew")
        
        # --- Buttons Area ---
        buttons_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=15, pady=15)
        buttons_frame.grid(row=1, column=0, sticky="nsew")
        
        # Configure button grid sizing
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
            
        # Button definitions: (Text, Row, Col, BgColor, FgColor)
        buttons = [
            ('AC', 0, 0, self.colors["btn_func_bg"], self.colors["btn_func_fg"]),
            ('C', 0, 1, self.colors["btn_func_bg"], self.colors["btn_func_fg"]),
            ('%', 0, 2, self.colors["btn_func_bg"], self.colors["btn_func_fg"]),
            ('/', 0, 3, self.colors["btn_op_bg"], self.colors["btn_op_fg"]),
            
            ('7', 1, 0, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('8', 1, 1, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('9', 1, 2, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('*', 1, 3, self.colors["btn_op_bg"], self.colors["btn_op_fg"]),
            
            ('4', 2, 0, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('5', 2, 1, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('6', 2, 2, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('-', 2, 3, self.colors["btn_op_bg"], self.colors["btn_op_fg"]),
            
            ('1', 3, 0, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('2', 3, 1, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('3', 3, 2, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('+', 3, 3, self.colors["btn_op_bg"], self.colors["btn_op_fg"]),
            
            ('+/-', 4, 0, self.colors["btn_func_bg"], self.colors["btn_func_fg"]),
            ('0', 4, 1, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('.', 4, 2, self.colors["btn_num_bg"], self.colors["btn_num_fg"]),
            ('=', 4, 3, self.colors["btn_eq_bg"], self.colors["btn_eq_fg"])
        ]
        
        self.btn_objects = {}
        for btn in buttons:
            text, r, c, bg, fg = btn
            
            b = tk.Button(
                buttons_frame, text=text, font=self.font_btn,
                bg=bg, fg=fg, activebackground=self._lighten_color(bg, 0.3),
                activeforeground=fg, borderwidth=0, relief="flat",
                command=lambda t=text: self._on_btn_click(t),
                cursor="hand2", takefocus=1
            )
            b.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            self.btn_objects[text] = b
            
            # Accessibility & Interaction Styles
            # Mouse hover
            b.bind("<Enter>", lambda e, btn=b, og_bg=bg: btn.configure(bg=self._lighten_color(og_bg)))
            b.bind("<Leave>", lambda e, btn=b, og_bg=bg: btn.configure(bg=og_bg))
            # Keyboard focus (Tab navigation)
            b.bind("<FocusIn>", lambda e, btn=b: btn.configure(highlightbackground=self.colors["focus_ring"], highlightthickness=3, highlightcolor=self.colors["focus_ring"]))
            b.bind("<FocusOut>", lambda e, btn=b: btn.configure(highlightthickness=0))

    def _lighten_color(self, hex_color, amount=0.15):
        """Utility to generate lighter variations of colors for hover effects."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(min(255, r + (255 - r) * amount))
        g = int(min(255, g + (255 - g) * amount))
        b = int(min(255, b + (255 - b) * amount))
        return f'#{r:02x}{g:02x}{b:02x}'
            
    def _bind_keys(self):
        """Binds physical keyboard inputs mapping to calculator buttons."""
        for key in '0123456789.+-*/%':
            self.root.bind(key, lambda event, char=key: self._on_btn_click(char))
            
        self.root.bind('<Return>', lambda event: self._on_btn_click('='))
        self.root.bind('<KP_Enter>', lambda event: self._on_btn_click('='))
        self.root.bind('<BackSpace>', lambda event: self._on_btn_click('C'))
        self.root.bind('<Escape>', lambda event: self._on_btn_click('AC'))
        self.root.bind('c', lambda event: self._on_btn_click('C'))
        self.root.bind('C', lambda event: self._on_btn_click('C'))
        self.root.bind('a', lambda event: self._on_btn_click('AC'))
        self.root.bind('A', lambda event: self._on_btn_click('AC'))
        
    def _update_display(self):
        """Refreshes the display and adjusts font size for responsiveness."""
        display_text = self.current_expr if self.current_expr else "0"
        
        # Adjust font size dynamically if the number gets too long to fit
        font_size = 48
        if len(display_text) > 10:
            # scale down but not below size 20
            font_size = max(20, 48 - (len(display_text) - 10) * 2)
            
        # Specific override if showing error
        if display_text == "Cannot be divided by zero":
            font_size = 20
        
        self.lbl_current.config(
            text=display_text, 
            font=('Inter', font_size, 'bold')
        )
        self.lbl_history.config(text=self.history_expr)
        
    def _clear_errors(self):
        """Resets the state if there's a pre-existing error before a new action."""
        if self.error_state:
            self.current_expr = ""
            self.history_expr = ""
            self.error_state = False
            self.last_operation_was_eval = False

    def _on_btn_click(self, char):
        """Handles core button logic routing."""
        # Always clear errors on any new meaningful keypress (unless it's just 'C' or 'AC')
        if char not in ('AC', 'C') and self.error_state:
            self._clear_errors()

        if char == 'AC':
            self.current_expr = ""
            self.history_expr = ""
            self.last_operation_was_eval = False
            self.error_state = False
            
        elif char == 'C':
            if self.error_state:
                self._clear_errors()
            elif self.last_operation_was_eval:
                self.history_expr = ""
                self.last_operation_was_eval = False
            else:
                self.current_expr = self.current_expr[:-1]
                
        elif char == '=':
            self._evaluate()
            
        elif char == '%':
            self._calculate_percentage()
            
        elif char == '+/-':
            if self.current_expr and self.current_expr != "0":
                if self.current_expr.startswith('-'):
                    self.current_expr = self.current_expr[1:]
                else:
                    self.current_expr = '-' + self.current_expr
                    
        elif char in '+-*/':
            if self.last_operation_was_eval:
                self.history_expr = self.current_expr + f" {char} "
                self.current_expr = ""
                self.last_operation_was_eval = False
            elif self.current_expr:
                if self.history_expr and not self.history_expr.endswith('='):
                    self._evaluate(internal=True)
                self.history_expr = self.current_expr + f" {char} "
                self.current_expr = ""
            elif self.history_expr and not self.history_expr.endswith('='):
                # Switch operator
                self.history_expr = self.history_expr[:-2] + f"{char} "
                
        else: # Numbers and Decimal
            if self.last_operation_was_eval:
                self.current_expr = char
                self.history_expr = ""
                self.last_operation_was_eval = False
            else:
                # Prevent multiple decimals
                if char == '.' and '.' in self.current_expr:
                    return
                # Replace initial zero
                if self.current_expr == '0' and char != '.':
                    self.current_expr = char
                else:
                    self.current_expr += char
        
        self._update_display()
        
    def _calculate_percentage(self):
        """Handles percentage logic"""
        if not self.current_expr:
            return
            
        try:
            if self.history_expr and not self.history_expr.endswith('='):
                parts = self.history_expr.strip().split()
                if len(parts) >= 2:
                    op1 = Decimal(parts[0])
                    current_val = Decimal(self.current_expr)
                    
                    if parts[1] in '+-':
                        val = op1 * (current_val / Decimal('100'))
                    else:
                        val = current_val / Decimal('100')
                        
                    self.current_expr = self._format_result(val)
                    return
            
            val = Decimal(self.current_expr) / Decimal('100')
            self.current_expr = self._format_result(val)
            
        except (InvalidOperation, ValueError):
            self.current_expr = "Error"
            self.error_state = True
            
    def _evaluate(self, internal=False):
        """Evaluates the mathematical expression."""
        if not self.history_expr or not self.current_expr:
            return
            
        if self.history_expr.endswith('='):
            return
            
        try:
            parts = self.history_expr.strip().split()
            if len(parts) < 2: return
            
            op1_str = parts[0]
            operator = parts[1]
            op2_str = self.current_expr
            
            op1 = Decimal(op1_str)
            op2 = Decimal(op2_str)
            
            if operator == '+':
                result = op1 + op2
            elif operator == '-':
                result = op1 - op2
            elif operator == '*':
                result = op1 * op2
            elif operator == '/':
                if op2 == 0:
                    raise ZeroDivisionError
                result = op1 / op2
                
            res_str = self._format_result(result)
            
            if not internal:
                self.history_expr = f"{op1_str} {operator} {op2_str} ="
                self.current_expr = res_str
                self.last_operation_was_eval = True
            else:
                self.current_expr = res_str
                
        except ZeroDivisionError:
            self.current_expr = "Cannot be divided by zero"
            self.error_state = True
        except (InvalidOperation, ValueError):
            self.current_expr = "Error"
            self.error_state = True

    def _format_result(self, val):
        """Removes trailing zeros to display clean integer and decimal values."""
        s = f"{val:f}"
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        return s

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
