package com.utils;

import org.springframework.stereotype.Service;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
@Service
public class ConnectionUtils {
    private HttpURLConnection connectToURL(String originalUrl) throws Exception {
        URL url = new URL(originalUrl);
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) url.openConnection();
        } catch (IOException e) {
            System.out.println("请求过于频繁，请一小时后再获取数据");
            e.printStackTrace();
        }
        connection.setConnectTimeout(10000);// 设置连接主机服务器超时时间：10000毫秒
        connection.setReadTimeout(60000);// 设置读取主机服务器返回数据超时时间：60000毫秒
        /*connection.setChunkedStreamingMode(5);*/// 设置重连次数为五次
        connection.setRequestMethod("GET");//请求方式为get
        /*connection.setRequestProperty("Content-Type", "application/json");*/
        return connection;
    }
        //获取输入的api的数据
        public String getJsonFromApi(String originalUrl) throws Exception {
            String result = "";
            HttpURLConnection connection = connectToURL(originalUrl);
            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {
                System.out.println("link ok");
                InputStream is = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
                //使用字符缓冲流，
                StringBuffer sbf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = br.readLine()) != null) {
                    sbf.append(temp);
                    sbf.append("\r\n");
                }

                result = sbf.toString();
                System.out.println(sbf);
            } else {
                System.out.println("link fault");
            }

            return result;
        }

        /*跳过防盗链*/
        public String skipReferer(String api, String referer) throws IOException {
            //String result = "https://api.bilibili.com/x/relation/followers?vmid=20736117&pn=1&ps=20&order=desc&jsonp=jsonp&callback=__jp5";
            String dataJSONP = null;
            URL url = new URL(api);
            HttpURLConnection connection = null;
            try {
                connection = (HttpURLConnection) url.openConnection();
            } catch (IOException e) {
                System.out.println("请求过于频繁，请一小时后再获取数据");
                e.printStackTrace();
            }
            //伪造referer
            connection.setRequestProperty("referer", referer);
            // 设置连接主机服务器超时时间：10000毫秒
            connection.setConnectTimeout(10000);
            // 设置读取主机服务器返回数据超时时间：60000毫秒
            connection.setReadTimeout(60000);
            //请求方式为get
            connection.setRequestMethod("GET");
            /*connection.setRequestProperty("Content-Type", "application/json");*/
            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {
                System.out.println("link ok");
                InputStream is = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                //使用字符缓冲流，
                StringBuffer sbf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = br.readLine()) != null) {
                    sbf.append(temp);
                    sbf.append("\r\n");
                }

                dataJSONP = sbf.toString();
                System.out.println(sbf);
            } else {
                System.out.println("link fault");
            }

            return dataJSONP;
        }

        public String getJsonFromApiByCook(String originalUrl, String cookie) throws Exception {
            String result = "";
            HttpURLConnection connection = connectToURL(originalUrl);
            connection.setRequestProperty("cookie", cookie);
            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {
                System.out.println("link ok");
                InputStream is = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
                //使用字符缓冲流，
                StringBuffer sbf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = br.readLine()) != null) {
                    sbf.append(temp);
                    sbf.append("\r\n");
                }

                result = sbf.toString();
                System.out.println(sbf);
            } else {
                System.out.println("link fault");
            }

            return result;
        }

        public String getJsonFromApiByHeader(String originalUrl, HashMap<String, String> headerMap) throws Exception {
            String result = "";
            HttpURLConnection connection = connectToURL(originalUrl);
            //设置请求头
            for (Map.Entry<String, String> entry:headerMap.entrySet()){
                connection.setRequestProperty(entry.getKey(), entry.getValue());
            }

            connection.setRequestMethod("GET");
            /*connection.setRequestProperty("Content-Type", "application/json");*/
            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {
                System.out.println("link ok");
                InputStream is = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8));
                //使用字符缓冲流，
                StringBuffer sbf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = br.readLine()) != null) {
                    sbf.append(temp);
                    sbf.append("\r\n");
                }

                result = sbf.toString();
                System.out.println(sbf);
            } else {
                System.out.println("link fault");
            }

            return result;
        }

        //发送请求并且携带参数
        public String request(String originalUrl, String data) throws IOException {
            String result = "";
            URL url = new URL(originalUrl);

            HttpURLConnection connection = null;
            try {
                connection = (HttpURLConnection) url.openConnection();
            } catch (IOException e) {
                System.out.println("请求过于频繁，请一小时后再获取数据");
                e.printStackTrace();
            }

            connection.setDoOutput(true);
            // 设置连接主机服务器超时时间：10000毫秒
            connection.setConnectTimeout(10000);
            // 设置读取主机服务器返回数据超时时间：60000毫秒
            connection.setReadTimeout(60000);
            //请求方式为get
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            //发送数据
            OutputStream outputStream = connection.getOutputStream();
            PrintWriter printWriter = new PrintWriter(outputStream);
            printWriter.println(data);
            printWriter.flush();

            // 通过连接对象获取一个输入流，向远程读取
            if (connection.getResponseCode() == 200) {
                System.out.println("link ok");
                InputStream is = connection.getInputStream();
                // 对输入流对象进行包装:charset根据工作项目组的要求来设置
                BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                //使用字符缓冲流，
                StringBuffer sbf = new StringBuffer();
                String temp = null;
                // 循环遍历一行一行读取数据
                while ((temp = br.readLine()) != null) {
                    sbf.append(temp);
                    sbf.append("\r\n");
                }

                result = sbf.toString();
                System.out.println(sbf);
            } else {
                System.out.println("link fault");
            }

            return result;
        }


}
