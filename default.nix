{ pkgs ? import <nixpkgs> {} }:
with pkgs.python3Packages;

buildPythonApplication {
  pname = "ksend";
  src = ./src;
  version = "0.2";
  propagatedBuildInputs = [ flask werkzeug ];
  UPLOAD_FOLDER = "/mnt/.share";
  HOSTNAME = "https://keltono.net/";
  FLASK_APP="ksend.py";
  
}
