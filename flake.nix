{
  inputs = {
    # nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    { systems, nixpkgs, ... }@inputs:
    let
      eachSystem = f: nixpkgs.lib.genAttrs (import systems) (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = eachSystem (pkgs: {
        default = pkgs.mkShell {
          buildInputs = [
            pkgs.nodejs
            
            pkgs.yarn

            pkgs.nodePackages.typescript
            pkgs.nodePackages.typescript-language-server

            pkgs.supabase-cli
            pkgs.docker

            pkgs.python312
            pkgs.python312Packages.requests
            pkgs.python312Packages.colorama
            pkgs.python312Packages.tqdm
          ];
        };
      });
    };
}