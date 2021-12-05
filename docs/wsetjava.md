#### Use case

    This module was created to quickly swap out java versions.
    Adding the path to the module (bin folder) to the PATH variable,
    allows execution from anywhere.

    When performing penetration tests, certain exploits required different
    java versions.
    In one case, java 8 was required, but burp suite only supports java 11,
    so swapping back and forth quickly saves time.

#### Sample module wsetjava - Change to specified java version on Kali

    First, ensure all needed Java versions are installed in /usr/bin/java
    Then in the wsetjava code, ensure that the path for each specified java
    version is as is on your system. Update if needed.
        JAVA_PATHS = {
            "java7": ["/usr/lib/jvm/jdk1.7.0_80/bin/java", "/usr/lib/jvm/jdk1.7.0_80/bin/javac"],
            "java8": ["/usr/lib/jvm/jdk1.8.0_301/bin/java", "/usr/lib/jvm/jdk1.8.0_301/bin/javac"],
            "java11": [
                "/usr/lib/jvm/java-11-openjdk-amd64/bin/java", "/usr/lib/jvm/java-11-openjdk-amd64/bin/javac"
            ]
        }
    Then run command: wsetjava -s java11

    wsetjava -s java11
        Setting version: java11
        Executing comand: update-alternatives --install '/usr/bin/java'
        'java' '/usr/lib/jvm/java-11-openjdk-amd64/bin/java' 0

        Executing comand: update-alternatives --install '/usr/bin/javac'
        'javac' '/usr/lib/jvm/java-11-openjdk-amd64/bin/javac' 0

        Executing comand: update-alternatives --set java /usr/lib/jvm/java-11-openjdk-amd64/bin/java
        update-alternatives: using /usr/lib/jvm/java-11-openjdk-amd64/bin/java to provide /usr/bin/java
        (java) in manual mode

        Executing comand: update-alternatives --set javac /usr/lib/jvm/java-11-openjdk-amd64/bin/javac
        update-alternatives: using /usr/lib/jvm/java-11-openjdk-amd64/bin/javac to provide /usr/bin/javac
        (javac) in manual mode

##### _All modules have helper flags -h and --help for more assistance._
