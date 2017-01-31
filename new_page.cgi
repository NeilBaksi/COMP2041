#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI ':standard';
use CGI::Session;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
warningsToBrowser(1);

use File::Basename;
use File::Path qw/make_path/;

#my @scriptpath=split(/\//,$0);
#my $scriptname = pop @scriptpath;


my @users = sort(glob("dataset-medium/*"));

print page_header();
print search_box();

print "<br>\n";


# the part for printing the new stuff==========

#my $name = param("name");

my $desc = param("description");
my $cdesc = param("commentdescription");
my $rdesc = param("replydescription");
#print "description is: $value<br>\n"; # line used for debugging
#print check_param();
print user_page($desc);
print page_trailer();
#==============================================

sub page_header {
    
    print "<!DOCTYPE html\n",
           "PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n",
          "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n",
   	      "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en-US\" xml:lang=\"en-US\">\n",
	      "<head>\n",
	        "<title>MATELOOK</title>\n",
	        "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\"/>\n",
	         "<link rel='stylesheet' href='my_matelook.css' type='text/css'/>\n",
		# Bootstrap start --> getbootstrap.com
		"<script src='//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js'></script>\n",
		"<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css'>\n",
		"<link href='//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css' rel='stylesheet'>\n",
		# Bootstrap end
		
		
		
         print header(-charset => "utf-8"),
        start_html(-title => 'MATELOOK', -style => "my_matelook.css",),
        div({-class => "matelook_heading"}, "matelook");
        print "<div class=\"container_lgout\">",
            "<p><a href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi\" class=\"btn btn-info btn-sm\">",
                "<span class=\"glyphicon glyphicon-log-out\"></span> Log out</a>",
            "</p>",
          "</div>"; 
        
}

sub user_page {

#to find out where the link is coming from using the url
#code from http://blog.techdex.net/How_to_get_the_current_URL_in_Perl.html
$page_url .= "://";
if ($ENV{SERVER_PORT} != "80") {
	$page_url .= $ENV{SERVER_NAME}.":".$ENV{SERVER_PORT}.$ENV{REQUEST_URI};
} else {
	$page_url .= $ENV{SERVER_NAME}.$ENV{REQUEST_URI};
}
    $user_id="";
	$user_id = $page_url;
	$user_id =~ s/(\:\/\/cgi\.cse\.unsw\.edu\.au\/~z5081777\/ass2\/new_page\.cgi\?value=)//g;
	$user_id =~ s/\%//;

	my $user_filename = "dataset-medium/$user_id/user.txt";
    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
   while ( my $line = <$fh> ) {         

        if ( $line =~ /(^full_name)/ ) {             
            $name = $line ;  
            $name =~ s/[\_]/ /g;
            $name =~ s/(full name=)/ /g;    
        }
        if ( $line =~ /(^zid)/ ) {             
            $zid = $line ;
            $zid =~ s/(zid=)/zID = /g;    
        }
        if ( $line =~ /(^program)/ ) {             
            $program = $line ;
            $program =~ s/(program=)/Program = /g ;      
        }
        if ( $line =~ /(^birthday)/ ) {             
            $birthday = $line ;
            $birthday =~ s/(birthday=)/Birthday = /g;      
        }
        if ( $line =~ /(^home_suburb)/ ) {             
            $home = $line ; 
            $home =~ s/[\_]/ /g;
            $home =~ s/(home suburb=)/Home Suburb = /g;     
        }
        if ( $line =~ /(^mates)/) {
            $mates = $line;
            $mates =~ s/[\[\]]/ /g;
            $umates = $mates;
            $umates =~ s/[^a-zA-Z0-9]/ /g;
            $umates =~ s/(^mates)//g;
            $umates =~ s/  z/ z/g; 
            $umates =~ s/^\s+|\s+$//g;
                        
        }
    }     
    close $fh;
    
    param('n', $n + 1);

    

    $image = "dataset-medium/$user_id/profile.jpg";
    unless (-e $image) {
       $image = "default/no_photo.jpg"; 
    } 

    print  "<div style='text-align:center; padding-top: 10px;'><img src='$image' alt='No Image' class='img-thumbnail'/></div>\n",
           '<p>',
            "<div class =\"matelook_user_details\">\n ",
            "<p style ='font-size:40px;font-weight:bold;'>$name<p>",
            "<p>$zid$program$birthday$home<p>",'<p>','<p>',
          "</div><p>";
   
          
    print   new_posts();
    print user_mates($user_id);
    
    start_form, "\n",
    hidden('n'), "\n",
    end_form, "\n";
    print print_new_posts();
    print user_posts($user_id);  
}

sub print_new_posts {

    #for time of when post is made
    @months = qw( 01 02 03 04 05 06 07 08 09 10 11 12 );
    # base code taken from www.tutorialspoint.com
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
    $year = $year -100;
    if($sec <= 10){
        $time = ("20$year-$months[$mon]-$mday T $hour:$min:0$sec+0000");
    }
    else {
        $time = ("20$year-$months[$mon]-$mday T $hour:$min:$sec+0000");
    }
    $time =~ s/( T )/T/g;
    if (defined $desc){
        if ($user_id =~ /(z[0-9]{7})/){
                $temp = $1;
                my $user_filename = "dataset-medium/$temp/user.txt";
                    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                    while ( my $line = <$fh> ) {         
                        if ( $line =~ /(^full_name)/ ) {             
                            $line =~ s/(full_name=)//;
                            $line =~ s/\s*$//;
                            $full_name = $line;
                            $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                            
                        }  	        
                    }close $fh;
                    $from=$user_id;
             $from =~ s/$temp/$full_name/g;
            }
            $desc = param("description");
            $desc =~ s/^\s+|\s+$//g;
            @messages = split / /,$desc;  
             
	         $k=0;
	        while ($k<=$#messages){             
                 if ($messages[$k] =~ /(z[0-9]{7})/){
                    $temp1 = $1;
                    my $user_filename = "dataset-medium/$temp1/user.txt";
                        open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                        while ( my $line = <$fh> ) {         
                            if ( $line =~ /(^full_name)/ ) {             
                                $line =~ s/(full_name=)//;
                                $line =~ s/\s*$//;
                                $full_name = $line;
                                $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                                $messages[$k] =~ s/$temp1/$full_name/g;
                            }  	        
                        }close $fh;
                     
                    }$k++;
                    $new_message = join(' ', @messages); 
                                
            }
            
        if (defined $desc){
        print "<div class =\"matelook_user_posts\">\n ",
                "<p>$time<p>from=$from<p>$new_message<p>",'<p>',
                "<div class =\"matelook_user_details\">\n ", 
                "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$temp\">",
                    "<p>",
                    "<TEXTAREA placeholder=\" Enter comment...\"name=\"commentdescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                    "<input type=\"submit\" name=\"submit\" value=\"Comment\">\n",
                    "</form></div>",   
              "</div>";
         # my $filename = $user_filename;
         # $filename=~ s/(user.txt)//;
         # $filename= $filename."/new_post.txt";
        #open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
        #print $fh "My first report generated by perl\n";
        #close $fh;
        }
    }
    
}
# check if using the . for concat removes errors <==================================== 
sub user_posts {
    
    my $i = 0;
    @temp = @_;
    @count =glob("dataset-medium/$temp[0]/posts/*");

    while ($i <= $#count){

        $temp[0] =~ s/(\/posts\/.*)//;
        $temp[0] =~ s/(dataset-medium\/)//;
        my $user_posts = "dataset-medium/$temp[0]/posts/$i/post.txt";
        open( my $fh, '<', $user_posts ) or die "Can't open $user_posts: $!";     
        while ( my $line = <$fh> ) {                    
            if ( $line =~ /(^from)/ ) {
                $from = $line;
            }
            if ( $line =~ /(^message)/ ) {             
                $message = $line ;
                $message =~ s/(message=)/ /g ;         
            }
            if ( $line =~ /(^time)/ ) {
                $time = $line;
                $time =~ s/(time=)/ /g ;
            }
         }     
         close $fh;
  
    if ($message =~ /(z[0-9]{7})/){
        $temp = $1;
        my $user_filename = "dataset-medium/$temp/user.txt";
            open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
            while ( my $line = <$fh> ) {         
                if ( $line =~ /(^full_name)/ ) {             
                    $line =~ s/(full_name=)//;
                    $line =~ s/\s*$//;
                    $full_name = $line;
                    $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                    $message =~ s/$temp/$full_name/g;

                }  	        
            }close $fh;
         
        }
       if ($from =~ /(z[0-9]{7})/){
            $temp = $1;
            my $user_filename = "dataset-medium/$temp[0]/user.txt";
                open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                while ( my $line = <$fh> ) {         
                    if ( $line =~ /(^full_name)/ ) {             
                        $line =~ s/(full_name=)//;
                        $line =~ s/\s*$//;
                        $full_name = $line;
                        $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                        
                    }  	        
                }close $fh;
         $from =~ s/$temp/$full_name/g;
        }
        $message =~ s/(\\n\\n)/<p>/g;
        $message =~ s/(\\n)/<br>/g;
        $temp1 = $time.'<p>'.$from;
        $temp1 = $temp1.'<p>';
        $temp1 = $temp1.$message;
        push @posts ,$temp1;
   
        $i++;
        # not entirely sure why temp[0] gets redefined but we need this code 
        $temp[0] =~ s/(\/posts\/.*)//;
        $temp[0] =~ s/(dataset-medium\/)//;
        @count =glob("dataset-medium/$temp[0]/posts/*");

    }
     @posts = reverse sort @posts;
     $x=0;
        
     while($x<= $#posts){
            print "<p>", 
                "<div class =\"matelook_user_posts\">\n ",
                     "<p>$posts[$x]<p>";
            print comments("dataset-medium/$temp[0]/posts/$x"); 
            print "<div class =\"matelook_user_details\">\n ", 
                "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$temp\">",
                    "<p>",
                    "<TEXTAREA placeholder=\" Enter comment...\"name=\"commentdescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                    "<input type=\"submit\" name=\"submit\" value=\"Comment\">\n",
                    "</form></div>",   
            "</div>";
            $temp[0] =~ s/(\/posts\/\d)//;
            $x++;   
    } 
    print user_mates_posts();
}
sub user_mates_posts{
    # smae code as user_mates that I used to make thumbnails
    my $wc = $umates =~ tr/ //; # count for number of ID's by couunter number of spaces
    $wc = $wc;
    my $i;
    my $j =0;
    my @name;
    while( $j <= $wc){
        my $temp = substr $umates,0+($j*9),8+($j*9);
        if ( $temp =~ /(z\d*)/){
            $temp = $1;
        }
        my $name = "";
   	    $user = "dataset-medium/$temp";
	    foreach (@users) {
            if ($_ =~ ($user)){
                $i=0;
                @cnt =glob("$user/posts/*");
	            while ($i <= $#cnt){
	                $user =~ s/(\/posts\/.*)//;
                    my $user_posts = "$user/posts/$i/post.txt";
                    open( my $fh, '<', $user_posts ) or die "Can't open $user_posts: $!";     
                        while ( my $line = <$fh> ) {                    
                            if ( $line =~ /(^from)/ ) {
                                $from = $line;
                            }
                            if ( $line =~ /(^message)/ ) {             
                                $message = $line ;
                                $message =~ s/(message=)/ /g ;         
                            }
                            if ( $line =~ /(^time)/ ) {
                                $time = $line;
                                $time =~ s/(time=)/ /g ;
                            }
                        }     
                        close $fh;
            if ($message =~ /(z[0-9]{7})/){
                $temp = $1;
                my $user_filename = "dataset-medium/$temp/user.txt";
                    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                    while ( my $line = <$fh> ) {         
                        if ( $line =~ /(^full_name)/ ) {             
                            $line =~ s/(full_name=)//;
                            $line =~ s/\s*$//;
                            $full_name = $line;
                            $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                            $message =~ s/$temp/$full_name/g;

                        }  	        
                    }close $fh;
                 
              }
            if ($from =~ /(z[0-9]{7})/){
                $temp = $1;
                my $user_filename = "dataset-medium/$temp/user.txt";
                    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                    while ( my $line = <$fh> ) {         
                        if ( $line =~ /(^full_name)/ ) {             
                            $line =~ s/(full_name=)//;
                            $line =~ s/\s*$//;
                            $full_name = $line;
                            $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                            
                        }  	        
                    }close $fh;
             $from =~ s/$temp/$full_name/g;
            }
            $message =~ s/(\\n\\n)/<p>/g;
            $message =~ s/(\\n)/<br>/g;
            $temp2 = $time.'<p>'.$from;
            $temp2 = $temp2.'<p>';
            $temp2 = $temp2.$message;

            push @mposts ,$temp2;
             $name[$i] = $temp;

            $i++;
            }
               @mposts = reverse sort @mposts;
               $y=0;
               $u="";
               while($y<= $#mposts){
                    if(defined $name[$y]){ 
                        $u = $name[$y];
                        $u =~ s/z/dataset-medium\/z/;
                        print "<div class =\"matelook_user_posts\">\n ",
                            "<p>$mposts[$y]<p>";
                        print comments("$u/posts/$y");
                        print "<div class =\"matelook_user_details\">\n ", 
                                 "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$name[$y]\">",
                                 "<p>",
                                 "<TEXTAREA placeholder=\" Enter comment...\"name=\"commentdescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                                 "<input type=\"submit\" name=\"submit\" value=\"Comment\">\n",
                                 "</form></div>",  
                            " </div>";
                    }
                $y++;
                }
          }           
        }  	    
	    $j++;   
    }

}

sub comments{
         @temp=@_;
         @count =glob("$temp[0]/comments/*");
         $j=0;
         while($j<= $#count){
             my $user_posts_comments = "$temp[0]/comments/$j/comment.txt";
             open( my $fh, '<', $user_posts_comments ) or die "Can't open $user_posts_comments: $!";     
             while ( my $line = <$fh> ) {                    
                if ( $line =~ /(^from)/ ) {
                    $cfrom = $line;
                }
                if ( $line =~ /(^message)/ ) {             
                    $cmessage = $line ;
                    $cmessage =~ s/(message=)/ /g ;         
                }
                if ( $line =~ /(^time)/ ) {
                    $ctime = $line;
                    $ctime =~ s/(time=)/ /g ;
                }
             }     
             close $fh;
             
        $cmessage =~ s/^\s+|\s+$//g;
         @cmessages = split / /,$cmessage;  
         
	     $k=0;
	    while ($k<=$#cmessages){             
             if ($cmessages[$k] =~ /(z[0-9]{7})/){
                $temp1 = $1;
                my $user_filename = "dataset-medium/$temp1/user.txt";
                    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                    while ( my $line = <$fh> ) {         
                        if ( $line =~ /(^full_name)/ ) {             
                            $line =~ s/(full_name=)//;
                            $line =~ s/\s*$//;
                            $full_name = $line;
                            $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp1">$line<\/a>/g;#/
                            $cmessages[$k] =~ s/$temp1/$full_name/g;
                        }  	        
                    }close $fh;
                 
                }$k++;
                $new_cmessage = join(' ', @cmessages);             
        }
        if ($cfrom =~ /(z[0-9]{7})/){
            $temp1 = $1;
            my $user_filename = "dataset-medium/$temp1/user.txt";
                open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                while ( my $line = <$fh> ) {         
                    if ( $line =~ /(^full_name)/ ) {             
                        $line =~ s/(full_name=)//;
                        $line =~ s/\s*$//;
                        $full_name = $line;
                        $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp1">$line<\/a>/g;#/
                        
                    }  	        
                }close $fh;
         $cfrom =~ s/$temp1/$full_name/g;
        }
       $cheat = $temp[0];
       $cheat =~ s/dataset-medium\/z[0-9]{7}//;
       $temp2 = $cheat.$ctime.'<p>'.$cfrom.'<p>'.$new_cmessage;
       push @comments ,$temp2;
       # print "<div class =\"matelook_user_details\">\n ",
       #     "<p>\t$cfrom\t$new_cmessage\n\t$ctime<p>",
       #    "</div>";  
        $j++;
       }   
   
       @comments = sort @comments;
       $i=0;

       while($i<= $#comments){
           $id = $temp[0];
           $id =~ s/(dataset-medium\/)//;
           $id =~ s/(\/posts\/\d)//;
	       $comments[$i] =~ s/(\/posts\/\d)//;
             print "<div class =\"matelook_user_details\">\n ",
                  "<p>\t$comments[$i]<p>",
                  "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$id\">",
                "<p>",
                "<TEXTAREA placeholder=\" Enter reply...\"name=\"commentdescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                "<input type=\"submit\" name=\"submit\" value=\"Reply\">\n",
                "</form>",
                    "</div>";
           print new_comments($id);
              $i++;        
       }
       @comments = ();
}

sub new_comments{
    @temp = @_;
    #for time of when comment is made
    @months = qw( 01 02 03 04 05 06 07 08 09 10 11 12 );
    # base code taken from www.tutorialspoint.com
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
    $year = $year -100;
    if($sec <= 10){
        $time = ("20$year-$months[$mon]-$mday T $hour:$min:0$sec+0000");
    }
    else {
        $time = ("20$year-$months[$mon]-$mday T $hour:$min:$sec+0000");
    }
    $time =~ s/( T )/T/g;
    
    if (defined $cdesc){
        if ($temp[0] =~ /(z[0-9]{7})/){
                $temp = $1;
                my $user_filename = "dataset-medium/$temp/user.txt";
                    open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                    while ( my $line = <$fh> ) {         
                        if ( $line =~ /(^full_name)/ ) {             
                            $line =~ s/(full_name=)//;
                            $line =~ s/\s*$//;
                            $full_name = $line;
                            $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                            
                        }  	        
                    }
                    close $fh;
                    $from=$temp[0];
                    $from =~ s/$temp/$full_name/g;
            }
            $cdesc = param("commentdescription");
            $cdesc =~ s/^\s+|\s+$//g;
            @messages = split / /,$cdesc;  
             
	         $k=0;
	        while ($k<=$#messages){             
                 if ($messages[$k] =~ /(z[0-9]{7})/){
                    $temp = $1;
                    my $user_filename = "dataset-medium/$temp/user.txt";
                        open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                        while ( my $line = <$fh> ) {         
                            if ( $line =~ /(^full_name)/ ) {             
                                $line =~ s/(full_name=)//;
                                $line =~ s/\s*$//;
                                $full_name = $line;
                                $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                                $messages[$k] =~ s/$temp/$full_name/g;
                            }  	        
                        }close $fh;
                     
                    }$k++;
                    $new_message = join(' ', @messages); 
                                
            }
            
        
        
        
        if (defined $cdesc){
        print "<div class =\"matelook_user_details\">\n ",
                "<p>$time\n from=$from\n$new_message<p>",'<p>',
                "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$id\">",
                    "<p>",
                    "<TEXTAREA placeholder=\" Enter reply...\"name=\"commentdescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                    "<input type=\"submit\" name=\"submit\" value=\"Reply\">\n",
                    "</form>",
              "</div>";
         }
    }
}


sub user_mates{         

    @data=@_;
    $data[0] =~ s/(dataset-medium\/)//;
    my $wc = $umates =~ tr/ //; # count for number of ID's by couunter number of spaces
    $wc = $wc+1;
    $unmate = param("unmate");
    $unmate =~ s/(UnMate )//; 
    $unmate =~ s/\?//;
    if (defined param("unmate")){
       $umates =~ s/$unmate //;
       $wc = $wc -1;
    }   
    my $j =0;
    while( $j lt $wc){
        my $temp = substr $umates,0+($j*9),8+($j*9);
        if ( $temp =~ /(z\d*)/){
            $temp = $1;
        }
        my $name = "";
   	    $user = "dataset-medium/$temp";
	    foreach (@users) {
            if ($_ =~ ($user)){
	            $user_filename = "$user/user.txt";
	            if ($user_filename =~ m/(dataset-medium\/\/user.txt)/){
                    print "<div class=\"alert alert-danger\" role=\"alert\">",
			        "<h1>You got no mates! :(</h1></div>\n";
			        print page_trailer();
			        exit;
                }
                open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                while ( my $line = <$fh> ) {         
                    if ( $line =~ /(^full_name)/ ) {             
                        $line =~ s/(^full_name)//;
                        $line =~ s/=//;
                        $line =~ s/\s*$//;
                        $name = $line;
                    }    
                } close $fh; 
            }         
        }  	    
       $image = "dataset-medium/$temp/profile.jpg";
       unless (-e $image) {
       $image = "default/no_photo.jpg"; 
       } 
   	    print "<marquee behavior=\"alternate\">",
	     " <div class=\"container\">\n",
 	       "<div class=\"row\">\n",
      	         "<div class=\"col-md-4\">",
      		   "<a class =\"thumbnail\" href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$temp\"><img src=\"$image\" alt=\"No Image\" style=\"width:150px;height:150px\"><p style='padding-left: 90px;'>$name</p></a>",
      		    "<form method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$data[0]\">",
      		   "<input type=\"submit\" name=\"submit\" value=\"UnMate?\"></form>",
    		   "</div></div></div></marquee>";
	    $j++;    
    }
	
# go to http://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_img_thumbnail2&stacked=h to fix css of user mates

	
}
   
 

sub new_posts {
	
    print   "<div class=\"matelook_user_details\"'>\n",
            "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$user_id\">",
                "<p>",
                "<TEXTAREA placeholder=\" Enter new post... \" name=\"description\" rows=\"5\" cols=\"100\"></TEXTAREA>\n",
                "<p>",
                "<input type=\"submit\" name=\"submit\" value=\"Post\">\n\n",
                "<p>",
                "<TEXTAREA placeholder=\" Search for post... \" name=\"search_posts\" rows=\"2\" cols=\"100\"></TEXTAREA>",
                "<p>",
                "<input type=\"submit\" name=\"search\" value=\"Search\">",
            "</FORM></div>";
}


sub search_box {
    print   "<div class=\"matelook_user_details\"'>\n",
            "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/search_results.cgi\">",
                "<p>",
                "<TEXTAREA placeholder=\" Search for mate... \" name=\"name\" rows=\"1\" cols=\"100\"></TEXTAREA>",
                "<p>",
                "<input type=\"submit\" name=\"submit\" value=\"Search\">",
            "</FORM></div>";
}





sub page_trailer {
    print "<marquee behavior=\"alternate\">COMP2041 Assignment 2 by Supratik Baksi- z5081777</marquee>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}


