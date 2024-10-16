with import <nixpkgs> {};
let
  #makeShell returns is assigned a _python_ function which returns a derivation 
  # which is defined between parenthesis ()
  makeShell = python: (mkShell {
    name = "py-env";

    buildInputs = with python.pkgs; [
      venvShellHook
    ];
    venvDir = ".venv${python.version}";
    postShellHook = ''
      - [ ] pip install -r requirements.txt
    '';
    }
  );
in
#from a single derivation to multiple derivations. To run just choose one; otherwise, it will fail when nix-shell is execute.
{
  #py39 = makeShell python39;
  #py310 = makeShell python310;
  #py311 = makeShell python311;
  py312 = makeShell python312;
}

## Run the above shell as:
## pyVersion is an attribute of the shell.nix attribute set.
#$pyVersion= 
#$nix-shell -A ${pyVersion} --run zsh
