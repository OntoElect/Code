package com.phd;
import java.io.File;
import java.io.IOException;

public class Main {

    private static void generateProxyListAndStart(DocumentFileReader fr,  String relative) throws IOException, InterruptedException {

        ProxyUtil.generateProxyList(new proxyCallback(){
            @Override
            public void onSuccess() throws IOException, InterruptedException {

                //clear all existed random numbers
                RandomUtil.getInstance().clearExistedRandomList();

                final File folder = new File(relative);
                fr.listFilesForFolder(folder);
            }

            @Override
            public void onError(String err) {
                // error happen
                System.out.println(err);
            }
        });
    }

    public static void main(String[] args) throws IOException, InterruptedException {

        DocumentFileReader fr = new DocumentFileReader();
        generateProxyListAndStart(fr, FileUtil.pathInput);
        CSVBuilder.getInstance().createCSV();
    }
}
