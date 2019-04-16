FROM centos:7

MAINTAINER Jun Futagawa <jfut@integ.jp>
LABEL maintainer="Jun Futagawa <jfut@integ.jp>"

RUN yum -y update && \
    yum -y groupinstall "Development Tools" && \
    yum -y install sudo wget git-core rpm-build rpmdevtools spectool yum-utils createrepo python-devel epel-release cabal-rpm && \
    yum clean all && \
    rm -rf /var/cache/yum

