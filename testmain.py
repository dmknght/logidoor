from datetime import datetime
from logidoor.new_libs.cli import options
from logidoor.new_libs.controller import do_attack
from logidoor.new_libs.cli import banner

if __name__ == "__main__":
    prog_options = options.ProgOptions()
    banner.program_banner()
    runtime = datetime.now()

    do_attack(prog_options)

    runtime = datetime.now() - runtime
    print(f"Elapsed: {runtime}")

