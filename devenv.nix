{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    hello

    # protobuf editor
    protoscope

    # Github Action Tester
    act
  ];

  languages.python = {
    enable = true;
    package = pkgs.python312;
    poetry = {
      enable = true;
      activate.enable = true;
    };
  };

  dotenv.enable = true;
  dotenv.filename = [".env"];

  enterShell = ''
    hello
  '';

  # On my machine the folder is on wsl windows path,
  # so i use git.exe on windows to replace the one on NixOS.
  # scripts.git.exec = "git.exe $@";
  # scripts.lgit.exec = "${pkgs.git}/bin/git $@";

  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  pre-commit.hooks = {
    alejandra.enable = true;

    isort.enable = true;
    autoflake.enable = true;
    mypy = {
      enable = true;
      excludes = [
        ".*yarn_spinner_pb2.py$"
        "yarn_spinner_pb2.py"
      ];
      args = [
        "--disable-error-code=attr-defined"
      ];
      extraPackages = with pkgs; [
        python312Packages.protobuf
        python312Packages.types-protobuf
      ];
    };
    # pylint.enable = true;
    # flake8.enable = true;
  };
}
