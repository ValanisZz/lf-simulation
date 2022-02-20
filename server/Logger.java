import java.io.FileWriter;
import java.text.DateFormat;
import java.util.Date;
import java.util.Locale;


public class Logger {

    private final FileWriter fileWriter;
    private final DateFormat dateFormat = new java.text.SimpleDateFormat("[dd.MM.yyyy | HH:mm:ss.SSS] ", new Locale("ru", "RU"));


    Logger(String filename) throws Exception {

        this.fileWriter = new FileWriter(filename, true);

    }


    protected void log(String message) throws Exception {

        log(message, true);

    }


    protected void log(String message, boolean addDate) throws Exception {

        if (addDate)
            message = dateFormat.format(new Date()) + message + "\n";

        fileWriter.write(message);
        fileWriter.flush();

    }

}
