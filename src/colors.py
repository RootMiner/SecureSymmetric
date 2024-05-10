
# Shell colors, originally these are light version of the colors
R = '\033[91m'  # Light Red
G = '\033[92m'  # Light Green
B = '\033[94m'  # Light Blue
C = '\033[96m'  # Cyan
Y = '\033[93m'  # Yellow
P = '\033[95m'  # Purple
r = '\033[0m'   # reset color value

# Shell Font Style
I = '\033[3m'  # Italic

# Success, Error and Question prompt color coding
S = f'{G}*{r}'
E = f'{R}!{r}'
Q = f'{Y}?{r}'
A = f'{P}+{r}'

# ------- Thinking of using it in future

# class ShellColors:
#     @classmethod
#     def success(cls, message): return f'{cls.G}{message}{cls.r}'

#     @classmethod
#     def error(cls, message): return f'{cls.R}{message}{cls.r}'

#     @classmethod
#     def question(cls, message): return f'{cls.Y}{message}{cls.r}'

