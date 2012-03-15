import java.io.*;
import java.net.*;
import java.util.Random;

public class test_case_moves {
	public static String script_dir(int player, int game, int move) {
		switch (player) {
			case 1: return player_1_dir(game,move);
			case 2: return player_2_dir(game,move);
			case 3: return player_3_dir(game,move);
			case 4: return player_4_dir(game,move);
		}
		return "";
	}
	
	private static String player_1_dir(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "N"; 
				case 2: return "S"; 
				case 3: return "E"; 
				case 4: return "W"; 
				case 5: return "W"; 
			}
		}
		else if (game == 1)
			return "N";
		else if (game == 2)
			return "N";
		else if (game == 3 || game == 4)
			return "N";
		else if (game == 5)
			return "NW";
		else if (game == 6)
			return "SE";
		else if (game == 7)
			return "SW";
		else if (game == 8) {
			switch (move) {
			case 1: return "SW";
			case 2: return "SE";
			}
		}
		else if (game == 9) {
			switch (move) {
			case 1: return "SE";
			case 2: return "SW";
			}
		}
		else if (game == 10) {
			switch (move) {
			case 1: return "S";
			case 2: return "SW";
			}
		}
		else if (game == 11) {
			return "S";
		}
		return "";
	}
	private static String player_2_dir(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "N"; 
				case 2: return "S"; 
				case 3: return "S"; 
				case 4: return "N"; 
				case 5: return "N"; 
			}
		}
		else if (game == 1)
			return "E";
		else if (game == 2)
			return "N";
		else if (game == 3 || game == 4)
			return "N";
		else if (game == 5)
			return "NW";
		else if (game == 6 || game == 7)
			return "S";
		else if (game == 8) {
			switch (move) {
			case 1: return "S";
			case 2: return "SE";
			}
		}
		else if (game == 9 || game == 10) {
			switch (move) {
			case 1: return "S";
			case 2: return "SW";
			}
		}
		else if (game == 11) {
			return "S";
		}
		return "";	
	}
	private static String player_3_dir(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "N"; 
				case 2: return "S"; 
				case 3: return "E"; 
				case 4: return "W"; 
				case 5: return "SW"; 
			}
		}
		else if (game == 1)
			return "S";
		else if (game == 2)
			return "S";
		else if (game == 3 || game == 4)
			return "N";
		else if (game == 5)
			return "NW";
		else if (game == 6|| game == 7)
			return "S";
		else if (game == 8) {
			switch (move) {
			case 1: return "S";
			case 2: return "SE";
			}
		}
		else if (game == 9  || game == 10) {
			switch (move) {
			case 1: return "S";
			case 2: return "SW";
			}
		}
		else if (game == 11) {
			return "S";
		}
		return "";
	}
	private static String player_4_dir(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "N"; 
				case 2: return "S"; 
				case 3: return "E"; 
				case 4: return "W"; 
				case 5: return "N"; 
			}
		}
		else if (game == 1)
			return "W";
		else if (game == 2)
			return "S";
		else if (game == 3)
			return "V";
		else if (game == 4)
			return "N";
		else if (game == 5)
			return "NW";
		else if (game == 6 || game == 7)
			return "S";
		else if (game == 8) {
			switch (move) {
			case 1: return "S";
			case 2: return "SE";
			}
		}
		else if (game == 9  || game == 10) {
			switch (move) {
			case 1: return "S";
			case 2: return "SW";
			}
		}
		else if (game == 11) {
			return "S";
		}
		return "";
	}
	
	public static String script_mag(int player, int game, int move) {
		switch (player) {
			case 1: return player_1_mag(game,move);
			case 2: return player_2_mag(game,move);
			case 3: return player_3_mag(game,move);
			case 4: return player_4_mag(game,move);
		}
		return "";
	}
	
	private static String player_1_mag(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "0"; 
				case 2: return "2"; 
				case 3: return "0"; 
				case 4: return "2"; 
				case 5: return "2"; 
			}
		}
		else if (game == 1)
			return "0";
		else if (game == 2)
			return "3";
		else if (game == 4)
			return "1";
		else if (game == 5)
			return "3";
		else if (game == 6 || game == 7)
			return "1";
		else if (game == 8 || game == 9)
			return "2";
		else if (game == 10 || game == 11)
			return "3";
		return "";		
	}
	private static String player_2_mag(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "0"; 
				case 2: return "1"; 
				case 3: return "2"; 
				case 4: return "1"; 
				case 5: return "1"; 
			}
		}
		else if (game == 1)
			return "0";
		else if (game == 2)
			return "3";
		else if (game == 4)
			return "1";
		else if (game == 5)
			return "3";
		else if (game == 6 || game == 7)
			return "2";
		else if (game == 8  || game == 9)
			return "3";
		else if (game == 10 || game == 11)
			return "3";
		return "";		
	}
	private static String player_3_mag(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "0"; 
				case 2: return "1"; 
				case 3: return "3"; 
				case 4: return "3"; 
				case 5: return "2"; 
			}
		}
		else if (game == 1)
			return "0";
		else if (game == 2)
			return "3";
		else if (game == 4)
			return "1";
		else if (game == 5)
			return "3";
		else if (game == 6 || game == 7)
			return "3";
		else if (game == 8  || game == 9)
			return "2";
		else if (game == 10)
			return "0";
		else if (game == 11)
			return "3";
		return "";		
	}
	private static String player_4_mag(int game, int move) {
		if (game == 0) {
			switch (move) {
				case 1: return "0"; 
				case 2: return "2"; 
				case 3: return "1"; 
				case 4: return "2"; 
				case 5: return "1"; 
			}
		}
		else if (game == 1)
			return "0";
		else if (game == 2)
			return "3";
		else if (game == 4)
			return "V";
		else if (game == 5)
			return "3";
		else if (game == 6 || game == 7 || game == 8  || game == 9)
			return "2";
		else if (game == 10)
			return "1";
		else if (game == 11)
			return "3";
		return "";	
	}
}
