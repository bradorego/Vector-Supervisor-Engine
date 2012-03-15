import java.io.*;
import java.net.*;
import java.util.Random;

public class computer_player {
    public static void main(String[] args) throws IOException {

    	String address = "localhost";
    	int port = 1337;
    	Random randy = new Random();
    	String identity = "CPU" + Integer.toString(randy.nextInt(99));
    	
    	if (args.length >= 1) {
    		address = args[0];
    	}
    	if (args.length >= 2) {
    		port = Integer.parseInt(args[1]);
    	}
    	if (args.length >= 3) {
    		identity = args[2];
    	}
    	
    	System.out.println(identity + "@" + address + ":" + port);
    	identity += "\r";
    	
        Socket echoSocket = null;
        PrintWriter out = null;
        BufferedReader in = null;

        try {
            echoSocket = new Socket(address, port);
            out = new PrintWriter(echoSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(
                                        echoSocket.getInputStream()));
        } catch (UnknownHostException e) {
            System.err.println("Don't know about Vector game server host.");
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for "
                               + "the connection to the Vector game server host.");
            System.exit(1);
        }

	BufferedReader stdIn = new BufferedReader(
                                   new InputStreamReader(System.in));
	String userInput;
	
	String line;
	
	//wait for the idenitfy signal
	while (true) {
		line = in.readLine();
		System.out.println(line);
		if (line.equals("IDENTIFY?")) {
			System.out.println("PRESENTING IDENTITY: " + identity);
			out.println(identity);
			break;
		}
	}
	
	String direction;
	String magnitude;
	String[] directions = {"N", "NE", "E", "SE", "S", "SW", "W", "NW"};
	
	//play the game
	while (true) {
		line = in.readLine();
		if (line == null) {
			System.out.println("TOURNAMENT OVER, DISCONNECTING");
			break;
		}
		if (!(line.equals("") || line == null))
			System.out.println(line);
		if (line.equals("DIRECTION?")) {
			direction = "DIRECTION: " + directions[randy.nextInt(7)] + "\r";
			System.out.println("PRESENTING " + direction);
			out.println(direction);
		}
		else if (line.equals("MAGNITUDE?")) {
			magnitude = "MAGNITUDE: " + Integer.toString(randy.nextInt(3)) + "\r";
			System.out.println("PRESENTING " + magnitude);
			out.println(magnitude);
		}
	}

	out.close();
	in.close();
	stdIn.close();
	echoSocket.close();
	System.exit(0);
    }
}
