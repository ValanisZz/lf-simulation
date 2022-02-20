import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;


public class Server {

    private ServerSocket serverSocket;
    private Socket clientSocket;

    private final Logger logger;


    @SuppressWarnings("ResultOfMethodCallIgnored")
    Server(String logFilename) throws Exception {

        File directory = new File("logs");

        if (!directory.exists())
            directory.mkdir();

        logger = new Logger(logFilename);

    }


    private void log(String message) {

        try {
            logger.log(message);
        } catch (Exception ignored) {}

    }


    public void start(int port) throws Exception {

        serverSocket = new ServerSocket(port);

        logger.log("\n---\n\n", false);
        log("Starting PLC Simulation Server");


        clientSocket = serverSocket.accept();


        log("Client connected - " + clientSocket);

        BufferedReader inFromClient = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));


        while (true) {
            if (inFromClient.ready()) {
                String message = inFromClient.readLine();
                System.out.println("The message sent from the socket was: " + message);
            }
        }

    }


    public static void main(String[] args) throws Exception {

        Server server = new Server("logs/main.log");

        new Thread(() -> {
            try {
                server.start(6666);
            } catch (Exception ignored) {}
        }).start();


        Scanner scanner = new Scanner(System.in);

        String inputText = "";

        System.out.println("PLC Simulation Server\n\nServer started, waiting for commands.\nAvailable commands: stop");


        while (true) {

            System.out.print("> ");

            inputText = scanner.next();

            if (inputText.equalsIgnoreCase("stop")) {
                server.log("Shutting down PLC Simulation Server");
                System.out.println("Terminating all active processes...");
                System.exit(0);
            }

        }

    }

}
