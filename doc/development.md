# Development

## Installing cabal-rpm

```
yum --enablerepo=epel install cabal-rpm
```

## Generate a spec file

- e.g.: contravariant-1.0

```
cabal-rpm spec contravariant-1.0
```

## GHC/Haskell Dependencies

List ghc dependencies in target packages.

### Current status: el7

```
# CentOS 7.6.1810: 2019-04-16
# ./package.sh -o no -uid
# ./package.sh -l
        "Crypto-4.2.5.1" -> "HUnit-1.2.5.2";
        "Crypto-4.2.5.1" -> "QuickCheck-2.6";
        "base-orphans-0.4.5" -> "base-4.6.0.1";
        "bifunctors-4.2.1" -> "semigroupoids-4.3";
        "comonad-4.2.7.2" -> "contravariant-1.0";
        "comonad-4.2.7.2" -> "distributive-0.4.4";
        "comonad-4.2.7.2" -> "semigroups-0.8.5";
        "contravariant-1.0" -> "tagged-0.8.4";
        "contravariant-1.0" -> "transformers-compat-0.3.3.4";
        "curl-1.3.8" -> "bytestring-0.10.0.2";
        "curl-1.3.8" -> "containers-0.5.0.0";
        "distributive-0.4.4" -> "tagged-0.8.4";
        "distributive-0.4.4" -> "transformers-compat-0.3.3.4";
        "generic-deriving-1.6.3" -> "template-haskell-2.8.0.0";
        "lens-3.10.3" -> "MonadCatchIO-transformers-0.3.0.0";
        "lens-3.10.3" -> "bifunctors-4.2.1";
        "lens-3.10.3" -> "filepath-1.3.0.1";
        "lens-3.10.3" -> "generic-deriving-1.6.3";
        "lens-3.10.3" -> "mtl-2.1.2";
        "lens-3.10.3" -> "parallel-3.2.0.3";
        "lens-3.10.3" -> "profunctors-4.4.1";
        "lens-3.10.3" -> "reflection-1.5.2.1";
        "lens-3.10.3" -> "split-0.2.2";
        "lens-3.10.3" -> "unordered-containers-0.2.3.0";
        "lens-3.10.3" -> "vector-0.10.0.1";
        "lens-3.10.3" -> "void-0.5.11";
        "profunctors-4.4.1" -> "semigroupoids-4.3";
        "reflection-1.5.2.1" -> "tagged-0.8.4";
        "regex-pcre-0.94.4" -> "regex-base-0.93.2";
        "semigroupoids-4.3" -> "comonad-4.2.7.2";
        "tagged-0.8.4" -> "template-haskell-2.8.0.0";
```

### Crypto

- http://hackage.haskell.org/package/Crypto
- cabal-rpm spec Crypto-4.2.5.1
- ./package.sh -p ghc-Crypto

### curl

- http://hackage.haskell.org/package/curl
- cabal-rpm spec curl-1.3.8
- ./package.sh -p ghc-curl

### regex-pcre

- http://hackage.haskell.org/package/regex-pcre
- cabal-rpm spec regex-pcre-0.94.4
- ./package.sh -p ghc-regex-pcre

### (base-orphans | tagged -> (contravariant | distributive) -> comonad)) -> semigroupoids

- http://hackage.haskell.org/package/base-orphans-0.4.5
  - Required: ghc-lens-3.10.3: base-orphans (<0.5)
- cabal-rpm spec base-orphans-0.4.5
- ./package.sh -p ghc-base-orphans

- http://hackage.haskell.org/package/tagged-0.8.4
  - EPEL ghc-transformers-compat: 0.3.3.4-3.el7
  - NG: 0.8.5 <= tagged: transformers-compat (>=0.5 && <1)
- cabal-rpm spec tagged-0.8.4
- ./package.sh -p ghc-tagged

```
# EPEL: ghc-tagged-0.6-2.el7
yum-config-manager --setopt="epel.exclude=ghc-tagged-*" --save epel
```

- http://hackage.haskell.org/package/contravariant-1.0
  - EPEL ghc-semigroups: 0.8.5-3.el7
  - EPEL ghc-transformers-compat RPM: 0.3.3.4-3.el7
  - tagged (>=0.4.4 && <1)
  - No foreign-var and StateVar
- cabal-rpm spec contravariant-1.0
- ./package.sh -p ghc-contravariant

- http://hackage.haskell.org/package/distributive-0.4.4
  - EPEL ghc-semigroups: 0.8.5-3.el7
  - EPEL ghc-transformers-compat: 0.3.3.4-3.el7
  - EPEL ghc-tagged: 0.6-2.el7 -> original tagged-0.8.4 RPM
  - NG: distributive <= 0.4.3.2: transformers-compat (==0.1.*)
  - OK: distributive = 0.4.4: Require tagged (>=0.7 && <1)
  - NG: 0.5 <= distributive: base-orphans (>=0.5 && <1)
  - No base-orphans and tagged
- cabal-rpm spec distributive-0.4.4
- ./package.sh -p ghc-distributive

- http://hackage.haskell.org/package/comonad-4.2.7.2
  - contravariant (>=0.2.0.1 && <2)
  - distributive (>=0.2.2 && <1)
  - semigroupoids-4.5: comonad (==4.*)
  - lens-3.10.3: comonad (==4.*)
  - NG: comonad-4.3: semigroupoids-4.2: Could not find module Data.Functor.Coproduct
  - NG: comonad-4.2.7.2: profunctors-4.0: In module `Data.Semigroupoid.Coproduct': `L' is a data constructor of `Coproduct''
- cabal-rpm spec comonad-4.2.7.2
- ./package.sh -p ghc-comonad

- http://hackage.haskell.org/package/semigroupoids-4.3
- cabal-rpm spec semigroupoids-4.3
  - base (>1 && <1)
  - base-orphans (>=0.3 && <1)
  - comonad (==4.*)
  - containers (>=0.3 && <0.6)
  - contravariant (>=0.2.0.1 && <2)
  - distributive (>=0.2.2 && <1)
  - semigroups (>=0.8.3.1 && <1)
  - transformers (>=0.2 && <0.6)
  - transformers-compat (>=0.3 && <0.5)
  - NG: comonad-4.3: semigroupoids-4.2 Could not find module Data.Functor.Coproduct
  - NG: semigroupoids-4.5: profunctors-4.0: In module `Data.Semigroupoid.Coproduct': `L' is a data constructor of `Coproduct''
  - OK: semigroupoids-4.3
- ./package.sh -p ghc-semigroupoids

### (bifunctors | profunctors | generic-derivin | reflectiong) -> lens

- http://hackage.haskell.org/package/bifunctors-4.2.1
  - Required: ghc-lens-3.10.3: bifunctors (==4.*)
- cabal-rpm spec bifunctors-4.2.1
- ./package.sh -p ghc-bifunctors

- http://hackage.haskell.org/package/profunctors-4.4.1
  - Required: ghc-lens-3.10.3: profunctors (==4.*)
  - NG: semigroupoids-4.5: In module `Data.Semigroupoid.Coproduct': `L' is a data constructor of `Coproduct''
- cabal-rpm spec profunctors-4.4.1
- ./package.sh -p ghc-profunctors

- http://hackage.haskell.org/package/generic-deriving
  - Required: ghc-lens-3.10.3: generic-deriving (>=1.4 && <1.7)
- cabal-rpm spec generic-deriving-1.6.3
- ./package.sh -p ghc-generic-deriving

yum install /pkg/rpmbuild/ghc-generic-deriving/RPMS/x86_64/ghc-generic-deriving-1.6.3-2.el7.x86_64.rpm /pkg/rpmbuild/ghc-generic-deriving/RPMS/x86_64/ghc-generic-deriving-devel-1.6.3-2.el7.x86_64.rpm

- http://hackage.haskell.org/package/reflection-1.5.2.1
  - NG: EPEL: ghc-reflection-1.4-1.el7 -> ghc-tagged-0.6-2.el7
  - Required: ghc-lens-3.10.3: reflection (>=1.1.6 && <2)
- cabal-rpm spec reflection-1.5.2.1
- ./package.sh -p ghc-reflection

```
# EPEL ghc-reflection-1.4-1.el7 -> ghc-tagged-0.6-2.el7
yum-config-manager --setopt="epel.exclude=ghc-tagged-* ghc-reflection-*" --save epel
```

- http://hackage.haskell.org/package/lens-3.10.3
  - base-orphans (<0.5)
  - bifunctors (==4.*)
  - comonad (==4.*)
  - distributive (>=0.3 && <1)
  - generic-deriving (>=1.4 && <1.7)
  - profunctors (==4.*)
  - reflection (>=1.1.6 && <2)
  - semigroupoids (==4.*)
  - NG: lens-4.10: ghc-constraints
- cabal-rpm spec lens-3.10.3
- ./package.sh -p ghc-lens

