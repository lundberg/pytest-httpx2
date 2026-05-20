{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    nixpkgs24.url = "github:nixos/nixpkgs/24.11";
    nixpkgsUnstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flakeUtils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, nixpkgs24, nixpkgsUnstable, flakeUtils }:
    flakeUtils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pkgs24 = nixpkgs24.legacyPackages.${system};
        pkgsUnstable = nixpkgsUnstable.legacyPackages.${system};
      in {
        packages = flakeUtils.lib.flattenTree {
          python310 = pkgs24.python310;
          uv = pkgs.uv;
        };
        devShell = pkgs.mkShell {
          buildInputs = with self.packages.${system}; [
            python310
            uv
          ];
          shellHook = ''
            [[ ! -d .venv ]] && \
              ${pkgs.uv}/bin/uv venv \
                --python python3.10 --allow-existing --relocatable --link-mode copy
            source .venv/bin/activate
          '';
        };
      }
    );
}
