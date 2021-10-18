package com.twitter.pojo;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
@Data
@Document(collection = "yyds")
public class TweetJSON {
    @Id
    private String _id;
    private String i;
}