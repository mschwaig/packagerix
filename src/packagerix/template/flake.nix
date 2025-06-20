{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in
   {

    packages.x86_64-linux.default = pkgs.callPackage ./package.nix {};
    packages.x86_64-linux.nixpkgs-src = nixpkgs.outPath;

  };
}
