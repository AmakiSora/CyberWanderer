import BiliBili.GetBiliBiliDynamic;
import FakerData.GetPersons;
import FakerData.GetProduct;

import java.util.Date;

public class CyberWandererApplication {
    public static void main(String[] args) throws Exception {
//        GetBiliBiliDynamic.getNotLoginDynamic();
//        GetBiliBiliDynamic.GetBiliBiliDynamic();
            GetPersons.get(600);
            GetProduct.get(600);
    }
}
