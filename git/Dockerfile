FROM ubuntu:16.04

RUN apt-get update && apt-get install -y git openssh-server

RUN useradd -m git
RUN mkdir /var/run/sshd
RUN echo /usr/bin/git-shell >> /etc/shells
RUN chsh -s /usr/bin/git-shell git
RUN echo git:git | chpasswd

CMD ["/usr/sbin/sshd", "-D"]
