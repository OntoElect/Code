package com.phd;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.FileReader;
import java.util.List;
import java.util.Random;


import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDDocumentCatalog;
import org.apache.pdfbox.pdmodel.PDDocumentInformation;
import org.apache.pdfbox.pdmodel.common.PDMetadata;


public class DocumentFileReader {



    public void listFilesForFolder(final File folder) throws IOException, InterruptedException {

        for (final File fileEntry : folder.listFiles()) {
            //System.out.println("fileEntry: " + fileEntry.getName());

            if (!fileEntry.getName().equals(".DS_Store")) {

                if (fileEntry.isDirectory()) {
                    listFilesForFolder(fileEntry);
                } else {
                    System.out.println(fileEntry.getName());

                    Random rand = new Random();
                    int sec = rand.nextInt(50000) + 30000;
                    Thread.sleep(sec);

                    readPdfFile(fileEntry);
                }
            }
        }

        TaskManager.getInstance().stop();
    }

    private void readPdfFile(File inFile) throws IOException {

        PDDocument document = PDDocument.load(inFile);

        if (!document.isEncrypted()) {
            PDDocumentInformation info = document.getDocumentInformation();
            PDDocumentCatalog catalog = document.getDocumentCatalog();
            PDMetadata metadata = catalog.getMetadata();

            System.out.println( "\n ======Info ======= \n" + metadata + "\n ============ \n");
            System.out.println( "\n Page Count= " + document.getNumberOfPages() );
            System.out.println( "Title= " + info.getTitle() );
            System.out.println( "Author= " + info.getAuthor() );
            System.out.println( "Subject=" + info.getSubject() );
            System.out.println( "Keywords=" + info.getKeywords() );
            System.out.println( "Creator=" + info.getCreator() );
            System.out.println( "CreationDate=" + info.getCreationDate().getWeekYear());
            System.out.println( "getMetadataKeys=" + info.getMetadataKeys() );

            String author = info.getAuthor();
            String subject = info.getTitle().trim();
            Integer createdDate = info.getCreationDate().getWeekYear();

            //To remove some info before title
            if(subject.contains(": "))  {
                subject = subject.split(": ")[1];
            }

            if (subject.length() > 0){
                performSearchInGoogleScholar(inFile.getName(), author, subject, createdDate);
            }
        }
        document.close();
    }

    private void performSearchInGoogleScholar(String filename, String author, String subject, Integer createdDate) throws IOException {

        GoogleScholar googleScholar = new GoogleScholar();
        Item item = googleScholar.getRecordsByAuthor(author, subject);

        String authors = "";
        if (author != null) {
           authors = author.replace(" "," ");
        }

        System.out.println("authors: " + authors);

        // If everything is fine: app will add to csv and move file to done
        if(item.citationCount > -1) {
            CSVBuilder.getInstance().buildCSV(item, filename, authors, subject, createdDate);
            FileUtil.moveToDone(filename);
        }
    }
}