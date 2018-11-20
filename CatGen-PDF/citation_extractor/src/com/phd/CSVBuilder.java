package com.phd;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Year;
import java.util.Arrays;

public class CSVBuilder {

    private static final CSVBuilder instance = new CSVBuilder();
    public static CSVBuilder getInstance() {
        return instance;
    }

    FileWriter writer = null;
    String pathCSV = new File("/var/data").toURI().relativize(new File("output/citation_final.csv").toURI()).getPath();

    public void createCSV() throws IOException {

        File file = new File(pathCSV);
        if (file.exists() && !file.isDirectory())
        {
            System.out.println("\n\n  FILE exists: ");
            writer = new FileWriter(file,true);//if file exists append to file. Works fine.
        }
        else
        {
            System.out.println("\n\n  FILE does not exist: ");
            writer = new FileWriter(pathCSV);
            CSVUtils.writeLine(writer, Arrays.asList("Total Citation", "No Citations", "paper file name", "author", "subject", "createdDate", "url", "error message"));
        }

        writer.flush();
        writer.close();
    }

   public void buildCSV(Item item, String filename, String author, String subject, Integer createdDate) throws IOException {

       Integer totalCitation = item.citationCount;
       String strNoCitations = totalCitation.toString();

       writer = new FileWriter(pathCSV, true);
       if(totalCitation > -1) {

           int currentYear = Year.now().getValue();
           //System.out.println("\n\n currentYear: " + currentYear);

           double noCitations = ((double) totalCitation / (double) (currentYear - createdDate - 1));
           //System.out.println("\n\n num noCitations: " + noCitations);

           strNoCitations = String.format("%.4f", noCitations);
           //System.out.println("\n\n str noCitations: " + strNoCitations);
       }

        CSVUtils.writeLine(writer, Arrays.asList(totalCitation.toString(), strNoCitations, filename, author, subject, createdDate.toString(), item.url, item.errorMessage),',', '"');

        writer.flush();
        writer.close();
    }

    public void closeCSV() throws IOException {
        writer.close();
    }
}
