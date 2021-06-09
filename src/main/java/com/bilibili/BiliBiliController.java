package com.bilibili;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BiliBiliController {
    @Autowired
    private GetBiliBiliDynamic getBiliBiliDynamic;
    @GetMapping("/getSomeDynamic")
    public String getSomeDynamic() throws Exception {
        getBiliBiliDynamic.getSomeDynamic(20);
        return "getSomeDynamic完成";
    }
    //http://localhost:4567/getUserDynamic?uid=1862400654&sum=20
    @GetMapping("/getUserDynamic")
    public String getUserDynamic(int uid,int sum) throws Exception {
        getBiliBiliDynamic.getUserDynamic(uid,sum);
        return "getUserDynamic完成";
    }
}
