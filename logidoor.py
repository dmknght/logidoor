from datetime import datetime
from logidoor.libs.cli import options
from logidoor.controller import do_attack
from logidoor.libs.cli import banner

if __name__ == "__main__":
    prog_options = options.ProgOptions()
    banner.program_banner()
    runtime = datetime.now()

    do_attack(prog_options)

    runtime = datetime.now() - runtime
    print(f"\n\033[97mElapsed\033[0m: \033[37m{runtime}\033[0m")
