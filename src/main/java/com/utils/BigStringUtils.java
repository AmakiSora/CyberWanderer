package com.utils;

import java.io.*;

public class BigStringUtils {
    public StringBuilder get(){
//        String Path = "D:\\cosmos\\test\\json.txt";//pc
        String Path = "/Users/cosmos/OneDrive/twitter/json.txt";//mac
        StringBuilder stringBuilder = new StringBuilder();
        try (FileReader reader =new FileReader(Path)){
            char[] chars = new char[32768];//一次性读取32768个字符
            int readCount;
            while ((readCount = reader.read(chars)) != -1){
//                System.out.println(new String(chars,0,readCount));
                stringBuilder.append(new String(chars,0,readCount));
            }
        }catch (IOException e){
            e.printStackTrace();
        }
//        try (InputStream inputStream = new FileInputStream(Path)) {
//            inputStream.read()
//        } catch (FileNotFoundException e) {
//            System.out.println("未找到文件");;
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        stringBuilder.append("");
        return stringBuilder;
    }
}
