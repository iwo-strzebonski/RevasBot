from getpass import getpass
from typing import Any

class CLIColors:  # pylint: disable=too-few-public-methods
    '''
    ANSI color codes used for printing colorful messages
    '''
    ENDC = '\033[0m'

    class Foreground:
        class Normal:
            BLACK       = '\033[30m'
            RED         = '\033[31m'
            GREEN       = '\033[32m'
            YELLOW      = '\033[33m'
            BLUE        = '\033[34m'
            MAGENTA     = '\033[35m'
            CYAN        = '\033[36m'
            WHITE       = '\033[37m'

        class Bright:
            BLACK       = '\033[90m'
            RED         = '\033[91m'
            GREEN       = '\033[92m'
            YELLOW      = '\033[93m'
            BLUE        = '\033[94m'
            MAGENTA     = '\033[95m'
            CYAN        = '\033[96m'
            WHITE       = '\033[97m'

    class Background:
        class Normal:
            BLACK       = '\033[40m'
            RED         = '\033[41m'
            GREEN       = '\033[42m'
            YELLOW      = '\033[43m'
            BLUE        = '\033[44m'
            MAGENTA     = '\033[45m'
            CYAN        = '\033[46m'
            WHITE       = '\033[47m'

        class Bright:
            BLACK       = '\033[100m'
            RED         = '\033[101m'
            GREEN       = '\033[102m'
            YELLOW      = '\033[103m'
            BLUE        = '\033[104m'
            MAGENTA     = '\033[105m'
            CYAN        = '\033[106m'
            WHITE       = '\033[107m'

class RevasConsole:
    @classmethod
    def ok(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Bright.GREEN}{mesg}{CLIColors.ENDC}')

    @classmethod
    def debug(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Bright.BLACK}{mesg}{CLIColors.ENDC}')

    @classmethod
    def warn(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Normal.YELLOW}{mesg}{CLIColors.ENDC}')

    @classmethod
    def error(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Bright.RED}{mesg}{CLIColors.ENDC}')

    @classmethod
    def header(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Bright.MAGENTA}{mesg}{CLIColors.ENDC}')

    @classmethod
    def list(cls, messages: list[Any]) -> None:
        for i, msg in enumerate(messages):
            print(
                f'{CLIColors.Background.Normal.MAGENTA}{i + 1}){CLIColors.ENDC} {CLIColors.Foreground.Normal.MAGENTA}{msg}{CLIColors.ENDC}'
            )

    @classmethod
    def info(cls, mesg: Any) -> None:
        print(f'{CLIColors.Foreground.Bright.CYAN}{mesg}{CLIColors.ENDC}')

    @classmethod
    def input(cls, mesg: Any) -> Any:
        return input(f'{CLIColors.Foreground.Bright.CYAN}{mesg}{CLIColors.ENDC}')

    @classmethod
    def getpass(cls, mesg: Any) -> Any:
        return getpass(f'{CLIColors.Foreground.Bright.CYAN}{mesg}{CLIColors.ENDC}')
