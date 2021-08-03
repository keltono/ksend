{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;

buildPythonApplication {
  pname = "app";
  src = ./src;
  version = "0.2";
  propagatedBuildInputs = [ flask werkzeug ];
}
