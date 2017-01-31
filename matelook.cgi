#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2016
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/matelook/

use CGI qw/:all/;
use CGI ':standard';
use CGI::Session;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
warningsToBrowser(1);
use File::Basename;
use File::Path qw(mkpath rmtree);


        #print header();
	    #print start_html(),
	    #p("--$_--$user--"),
	    # end_html();
my $users_dir = "dataset-medium";
my $n = param('n') || 0;
my @users = sort(glob("$users_dir/*"));
my $user_to_show  = $users[$n % @users];
$loginFlag = 0;

$cgi = CGI->new;
(!defined param('logoutbtn')) ? ($sid = $cgi->cookie("CGISESSID") || undef) : ($sid = undef);
$session = new CGI::Session(undef, $sid, {Directory=>'/tmp'});
$session->expire('+30m');
$loggedIn = $session->param('loggedIn') || 0;
$cookie = $cgi->cookie(-name => 'CGISESSID', -value => $session->id, -expires => '+30m');
if (defined param('loginbtn')) {
    my $username_found = 0;
    my @users = sort(glob("$users_dir/*"));
	my $user = param('loginUser');
	my $password = param('loginPass');

	$user = "dataset-medium/$user";
	foreach (@users) {
		if ($_ =~ ($user)){
		    $username_found = 1;
	    }
	}

	if ($username_found eq 1){
	    my $user_filename = "$user/user.txt";
        open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
        while ( my $line = <$fh> ) {         
            if ( $line =~ /(^password)/ ) {             
                $line =~ s/(^password)//;
                $line =~ s/=//;
                $line =~ s/\s*$//;
 
                if ($line eq $password){
                    $session->param('loggedIn', 1);
    	            $loggedIn = 1;
	        	    $session->param('username', $user);
		            $loginFlag = 1; 

                }    
            }
        }         
        close $fh;
    }
    if ($loggedIn eq 0) { 
		print page_header();
		$loginFlag = 1;
		print "<div class=\"alert alert-danger\" role=\"alert\">",
			"Oops, looks like your username or password is wrong. Please try again.</div>\n";
	}
	
	
}

#if (defined param('logoutbtn')) {
#	$session->param('loggedIn', 0);
#	$session->clear('scores');
#	$loggedIn = 0;
#}
if (!$loggedIn) {
	#print header() if (!$loginFlag);
	print page_header() if (!$loginFlag);
	print login_page();
} else {
	$username = $session->param('username') if (!defined $username);
	#print $session->header();
	print page_header();
	print search_box();
	print user_page($username);
}


print page_trailer();
#
# Show user for user "n".
# Increment parameter n and store it as a hidden variable
#
sub user_page {
    print "<div class=\"container_lgout\">",
            "<p><a href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/matelook.cgi\" class=\"btn btn-info btn-sm\">",
                "<span class=\"glyphicon glyphicon-log-out\"></span> Log out</a>",
            "</p>",
          "</div>";   

	@user_id = @_;
	$del = $user_id[0];
	$del =~ s/(dataset-medium\/)//;
	print "<div class=\"container_del\">",
            "<p><a href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/delete_user.cgi?value=$del\" class=\"btn btn-info btn-sm\">",
                "<span class=\"glyphicon glyphicon-floppy-remove\"></span>Delete User?</a>",
            "</p>",
          "</div>";  
     #save new post in directory
 
   # my $filename = "/dataset-medium/a";
    #my $dirname = dirname($filename);
   # make_path 'dataset-medium/a';
   # open my $fh, '>', $filename or die "Could not open file '$filename' $!";
   # print $fh "Random test text\n";
   #close $fh;
    ###############################
    
 
    my $user_filename = "$user_id[0]/user.txt";
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
    $image = "$user_id[0]/profile.jpg";
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
    
            start_form, "\n",
            hidden('n'), "\n",
            end_form, "\n";
    print user_mates($user_id[0]);        
    print user_posts($user_id[0]); 

}

sub user_posts {
    
    my $i = 0;
    @temp = @_;
    
    @count =glob("$temp[0]/posts/*");

    while ($i <= $#count){
	    $temp[0] =~ s/(\/posts\/.*)//;
        my $user_posts = "$temp[0]/posts/$i/post.txt";

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
         $message =~ s/^\s+|\s+$//g;
         @messages = split / /,$message;  
         
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
        $new_message =~ s/(\\n\\n)/<p>/g;
        $new_message =~ s/(\\n)/<br>/g;
        $temp1 = $time.'<p>'.$from;
        $temp1 = $temp1.'<p>';
        $temp1 = $temp1.$new_message;
        push @posts ,$temp1;
        # not entirely sure why temp[0] gets redefined but we need this code 
        $temp[0] =~ s/(\/posts\/.*)//;
        @count =glob("$temp[0]/posts/*");
        $i++;
          
     }
      @posts = reverse sort @posts;
      $x=0;
        
       while($x<= $#posts){
        print "<p>", 
            "<div class =\"matelook_user_posts\">\n ",
                 "<p>$posts[$x]<p>";
        $data = $temp[0];
        $data =~ s/(dataset-medium\/)//;

        print "<form method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$data\">",
      		   "<input type=\"submit\" name=\"delete\" value=\"Delete Post $x?\"></form>";

        if (defined param("delete")){
            rmdir "$temp[0]/posts/$x";
        }

        print comments("$temp[0]/posts/$x"); 
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
      
  #
   print user_mates_posts();
}
sub user_mates_posts{
    # same code as user_mates that I used to make thumbnails
    print "<h2>Mates posts :</h2>";
    my $wc = $umates =~ tr/ //; # count for number of ID's by couunter number of spaces
    $wc = $wc;
    
    my $i;
    my $j =0;
    my $k =0;
    my @name;
    while( $j <= $wc){
        my $temp1 = substr $umates,0+($j*9),8+($j*9);
        if ( $temp1 =~ /(z\d*)/){
            $temp1 = $1;
        }
        my $name = "";
   	    $user = "dataset-medium/$temp1";
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
                        
         
                         $message =~ s/^\s+|\s+$//g;
                         @messages = split / /,$message;  
         
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
                            $new_message =~ s/(\\n\\n)/<p>/g;
                            $new_message =~ s/(\\n)/<br>/g;          
                    }
                   if ($from =~ /(z[0-9]{7})/){
                        $temp = $1;
                        my $user_filename = "$user/user.txt";
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
                    $temp2 = $time.'<p>'.$from;
                    $temp2 = $temp2.'<p>';
                    $temp2 = $temp2.$new_message;
                    push @mposts ,$temp2;

                      
                        $name[$i] = $user;
                        $name[$i] =~ s/(dataset-medium\/)//;
                        $i++;
                  }
                   @mposts = reverse sort @mposts;
                   $y=0;
                   my $u="";
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
	            $j++;   
        }
      }
    }
    print tagged_posts();
}
sub tagged_posts{

    $a=0;
    
   while ($a<=$#users) {
        $id = $users[$a];
        $id=~ s/(dataset-medium\/)//g;
        @count =glob("dataset-medium/$id/posts/*");
	     $b=0;
        while ($b<=$#count){
        
            my $user_posts = "dataset-medium/$id/posts/$b/post.txt";
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
                    $time = $time;
                    $time =~ s/(time=)/ /g ;
                }
             }     
             close $fh;
             $message =~ s/^\s+|\s+$//g;
            @messages = split / /,$message;  
         
	        $c=0;
	        while ($c<=$#messages){             
                if ($messages[$c] =~ /(z[0-9]{7})/){
                    $temp = $1;
                    my $user_filename = "dataset-medium/$temp/user.txt";
                        open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                        while ( my $line = <$fh> ) {         
                            if ( $line =~ /(^full_name)/ ) {             
                                $line =~ s/(full_name=)//;
                                $line =~ s/\s*$//;
                                $full_name = $line;
                                $full_name =~ s/^.*$/<a href="http:\/\/cgi.cse.unsw.edu.au\/~z5081777\/ass2\/new_page.cgi?value=$temp">$line<\/a>/g;#/
                                $messages[$c] =~ s/$temp/$full_name/g;
                            }  	        
                        }close $fh;
                     
                    }$c++;
                    $new_message = join(' ', @messages);                  
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
                    }
                    close $fh;
                    $from =~ s/$temp/$full_name/g;
            }
            $name = param('loginUser');
            $nameid = $name;
            if ($name =~ /(z[0-9]{7})/){
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
                    $name =~ s/$temp/$full_name/g;
            }
             
             $new_message =~ s/(\\n\\n)/<p>/g;
             $new_message =~ s/(\\n)/<br>/g;
             if(($new_message=~ /$name/i)||($new_message=~ /$nameid/i)){
                $temp = $time.'<br>'.$from.'<br>'.$new_message;
                push @tagged_posts ,$temp;
            }
        

            $b++;
         }
         $a++;
    }
    @tagged_posts = reverse sort @tagged_posts;
    $d=0;
    print "<h2>Tagged posts :</h2>";
    while ($d <= $#tagged_posts){
         print"<div class =\"matelook_user_posts\">\n ",
                 "<p>$tagged_posts[$d]<p>",
              "</div>";
	     $d++;  
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
                $new_message =~ s/(\\n\\n)/<p>/g;
                $new_message =~ s/(\\n)/<br>/g;            
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
        #$address[$j] = $cheat;  
        $j++; 
       }   
   
       @comments = sort @comments;
       $i=0;

       while($i<= $#comments){
            my $id = param('loginUser');
            #$reply = "dataset-medium/$id$address[$i]/comments/$i";

            $comments[$i] =~ s/(\/posts\/\d)//;
            
            
            
            
            
            
             print "<div class =\"matelook_user_details\">\n ",
                  "<p>\t$comments[$i]<p>";

             print "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$id\">",
                "<p>",
                "<TEXTAREA placeholder=\" Enter reply...\"name=\"replydescription\" rows=\"1\" cols=\"100\"></TEXTAREA>\n",
                "<input type=\"submit\" name=\"submit\" value=\"Reply\">\n",
                "</form>",
                    "</div>";

              $i++;        
       }
       @comments = ();
}


sub user_mates{         
    @data=@_;
    $data[0] =~ s/(dataset-medium\/)//;
    my $wc = $umates =~ tr/ //; # count for number of ID's by counter number of spaces
    $wc = $wc+1;
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
                open( my $fh, '<', $user_filename ) or die "Can't open $user_filename: $!";     
                while ( my $line = <$fh> ) {         
                    if ( $line =~ /(^full_name)/ ) {             
                        $line =~ s/(^full_name)//;
                        $line =~ s/=//;
                        $line =~ s/\s*$//;
                        $name = $line;
                    }    
                }close $fh;
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
      		   "<a class =\"thumbnail\" href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$temp\"><img src=\"$image\" alt=\"No Image\" style=\"width:150px;height:150px\"><p style='padding-left: 65px;'>$name</p></a>",
      		   "<form method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$data[0]\">",
      		   "<input type=\"submit\" name=\"unmate\" value=\"UnMate $temp?\"></form>",
    		   "</div></div></div></marquee>";
	    $j++;    
    }
	
# go to http://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_img_thumbnail2&stacked=h to fix css of user mates

	
}


sub new_posts {
    
    #save new post in directory
 
   # my $filename = "/import/ravel/3/z5081777/public_html/ass2/dataset-medium/a";
    #my $dirname = dirname($filename);
  #  mkdir $filename;
  #  open my $fh, '>', $filename or die "Could not open file '$filename' $!";
  #  print $fh "Random test text\n";
 #   close $fh;

    
    
    my $id = param('loginUser');
    print   "<div class=\"matelook_user_details\"'>\n",
                "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$id\">",
                "<p>",
                "<TEXTAREA placeholder=\" Enter new post... \"name=\"description\" rows=\"5\" cols=\"100\"></TEXTAREA>\n",
                "<p>",
                "<input type=\"submit\" name=\"submit\" value=\"Post\">\n\n",
                "</form>",
                "<form action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_page.cgi?value=$id\">",
                  "<input type=\"file\" name=\"pic\" accept=\"image/*\">",
                  "<input type=\"submit\">",
                "</form>",
                "<form  method=\"post\" action=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/search_results.cgi\">",
                "<p>",
                "<TEXTAREA placeholder=\" Search for post... \" name=\"search_posts\" rows=\"2\" cols=\"100\"></TEXTAREA>",
                "<p>",
                "<input type=\"submit\" name=\"search\" value=\"Search\"><p>",
            "</form></div>";
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
        start_html(-title => 'MATELOOK', -style => "color:white; my_matelook.css"),
        div({-class => "matelook_heading"}, "matelook");
        
}


sub login_page {
	# START BOOTSTRAP SIGNIN -> getbootstrap.com/examples/signin
	
	print 
	"<div class=\"container\" style='padding-top: 0px; color: rgb(106,150,242); '>\n",
     	  "<form class=\"form-signin\" role=\"form\" method='POST'>\n",
            "<h1 class=\"form-signin-heading\">Please login</h1>\n" ,
              "<input type=\"username\" class=\"form-control\" placeholder=\"Username\" name='loginUser' required=\"autofocus\">\n",'<p>',
              "<input type=\"password\" class=\"form-control\" placeholder=\"Password\" name='loginPass' required>\n",'<p>',
             "<label class=\"checkbox\" style='padding-left: 20px'>\n",
               "<input type=\"checkbox\" value=\"remember-me\"> Remember me</label>\n",
                "<h4><a style='padding-left: 20px;' href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/forgot_password.cgi\">Forgot Password</a></h4><p>" ,
                "<h4><a style='padding-left: 50px;' href=\"http://cgi.cse.unsw.edu.au/~z5081777/ass2/new_user.cgi\">Sign Up!</a></h4><p>" ,
             "<button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\" name='loginbtn'>Login</button>\n",
      	   "</form></div>\n";
    # END BOOTSTRAP SIGNIN 

}
    
#}

#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
    print "<marquee behavior=\"alternate\">COMP2041 Assignment 2 by Supratik Baksi- z5081777</marquee>";
    my $html = "";
    $html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
    $html .= end_html;
    return $html;
}

