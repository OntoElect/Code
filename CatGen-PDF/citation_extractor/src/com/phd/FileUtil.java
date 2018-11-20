package com.phd;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;


public class FileUtil {

    static String base = "/var/data";
    static String pathInput = new File(base).toURI().relativize(new File("input").toURI()).getPath();
    static String pathDone = new File(base).toURI().relativize(new File("tmp_done").toURI()).getPath();

    public static void moveToDone(String filename) throws IOException {

        String from = pathInput + filename;
        String to = pathDone + filename;

        System.out.println("from: " + from);
        System.out.println("to: " + to);

        Files.move(Paths.get(from), Paths.get(to), StandardCopyOption.REPLACE_EXISTING);
    }
}