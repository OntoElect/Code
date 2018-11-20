package com.phd;

import java.io.IOException;


import java.net.*;
import java.util.prefs.Preferences;
import java.util.regex.Pattern;

import org.jsoup.*;
import org.jsoup.Connection.Response;
import org.jsoup.nodes.*;
import org.jsoup.select.*;

import java.util.*;

public class GoogleScholar {

    private int maxConnections = 999999; //15;

    public static class TooManyConnectionsException extends IOException {
        private static final long serialVersionUID = 51944780478954114L;

        TooManyConnectionsException(String message) {
            super(message);
        }
    }

    private static void addHeader(Connection conn) {
        conn.header("User-Agent", "Mozilla");
        conn.header("Accept", "text/html,text/plain");
        conn.header("Accept-Language", "en-us,en");
        conn.header("Accept-Encoding", "gzip");
        conn.header("Accept-Charset", "utf-8");
    }

    public void clearCookies() {
        Preferences pref = Preferences.userRoot().node(
                GoogleScholar.class.getName());
        pref.remove("cookie");
    }

    private static Pattern authorPattern = Pattern.compile("[a-zA-Z ]*");

    public Item getRecordsByAuthor(String author, String subject)
            throws IOException {

        String url = "http://scholar.google.com/scholar?start=0&num=1&hl=en&as_sdt=0";

        //Build  query
        if (author != null) {
            String subj = URLEncoder.encode(subject, "UTF-8");
            url += "&q=" + subj;

            String aut = URLEncoder.encode(author, "UTF-8");
            url += "%22+author%3D%22" + aut + "%22&btnG=";
        } else {
            String subj = URLEncoder.encode(subject, "UTF-8");
            url += "&q=" + subj;
            url += "%22&btnG=";
        }

        System.out.println("url: " + url);
        return getCitesByUrl(url);
    }

    public Item getCitesByUrl(String url) throws IOException {

        Item item = new Item();
        item.url = url;
        item.errorMessage = "";

        Document doc = getDocument(url);
        if (doc == null) {
            System.out.println("document reading error: " + url);
            item.citationCount = -1;
            item.errorMessage = "Document reading error";
            return item;
        }
        System.out.println("DOC: " + doc);

        Elements elements = doc.select("div.gs_r");

        System.out.println("element size: " + elements.size());
        if (elements.size() == 0) {
            item.citationCount = -1;
            item.errorMessage = "Document elements.size() == 0";
            return item;
        }
        for (Element element : elements) {
            Elements links = element.select(".gs_fl a[href]");

            int countNotFound = 0;
            for (Element link : links) {
                 if (link.attr("href").contains("cites=")){
                     item.citationCount = Integer.parseInt(link.text().replace("Cited by ",""));
                     return item;
                 } else {
                    countNotFound ++;
                }

            }
            //If app checked every link but found nothing
            if (links.size() == countNotFound) {
                item.citationCount = 0; //no cites
                item.errorMessage = "no cites";
                return item;
            }

        }

        item.citationCount = -1;
        item.errorMessage = "Cannot found cites= element";
        return item;
    }

    public Document getDocument(String url) throws IOException {

        if (--maxConnections <= 0)
            throw new TooManyConnectionsException(
                    "Too many Google Scholar HTML requests");

        Preferences pref = Preferences.userRoot().node(
                GoogleScholar.class.getName());

        String cookie = pref.get("cookie", "");
        if (!cookie.contains("GSP")) {
            Connection conn = Jsoup
                    .connect("http://scholar.google.com/scholar_ncr");
            addHeader(conn);

            conn.get();

            Response resp = conn.response();
            cookie = "PREF=" + resp.cookie("PREF");
            cookie += "; GSP=" + resp.cookie("GSP") + ":CF=4";

            pref.put("cookie", cookie);
        }

        List<CPProxy> res = ProxyUtil.CPProxyList;
        Integer index = RandomUtil.getInstance().generateRandom(res.size()-1);
        CPProxy cpProxy = res.get(index);

        Connection conn = Jsoup.connect(url).proxy(cpProxy.adress,Integer.valueOf(cpProxy.port));
        addHeader(conn);
        conn.header("Cookie", cookie);


        Document doc = null;
        try {
            doc = conn.get();
            return doc;
        } catch (Exception e) {
            System.out.println("connection error:" + e.getLocalizedMessage());
        }

        return doc;
    }
}
