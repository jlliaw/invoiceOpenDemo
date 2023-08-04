package my.invoice;

import java.io.*;
import java.net.*;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

public class Program 
{
    public static void main( String[] args )
    {
        Program me = new Program();
        me.getInvoiceData();
    }

	



    private void getInvoiceData()
    {
        String apiurl = "https://dataset.einvoice.nat.gov.tw/ods/portal/api/v1/PrizeStaticByCity?yearNm=%s&hsnNm=%s&prizeNm=%s&offset=%s";
        String targetURL = apiurl;

		String[] processYears = {"2019", "2020", "2021", "2022", "2023"};
		String[] county = {"宜蘭縣","花蓮縣","金門縣","南投縣","屏東縣","苗栗縣","桃園市","高雄市","基隆市","連江縣","雲林縣","新北市","新竹市","新竹縣","嘉義市","嘉義縣","彰化縣","臺中市","臺北市","臺東縣","臺南市","澎湖縣"};
		String[] prize = {"二獎","三獎","千萬特獎","五獎","六獎","四獎","特獎","雲端發票八百元獎","雲端發票五百元獎","雲端發票百萬元獎","雲端發票兩千元獎","頭獎"};
        	        
        int offset = 0;
        int returnLength = 0;
        for(String y : processYears )
        {       
			for(String c: county)  
			{
				for(String p: prize)
				{
					do
					{
						try {
							targetURL = String.format(apiurl, y, URLEncoder.encode(c,"UTF-8"), URLEncoder.encode(p, "UTF-8"), offset);
						} catch (UnsupportedEncodingException e) {							
							e.printStackTrace();
						}				
						JsonElement jsonelement = JsonParser.parseString(apiFetch(targetURL));
						JsonArray jsonArray = jsonelement.getAsJsonArray();				
						returnLength = jsonArray.size();   
		
						System.out.println(String.format("year: %s, county: %s, prize: %s, return count: %s", y, c, p, returnLength));
			
						if (returnLength == 0)
						{
							//沒有資料回傳, offset清掉
							offset = 0;
							continue;
						}
						else
						{
							offset += jsonArray.size();
							dataConverter(jsonArray);					            
						}            			
					}while(returnLength > 0);
				}
			}


        }
    }

    private String apiFetch(String apiurl)
    {
        //JSONArray jsonarray = null;
        URL url = null;
		HttpURLConnection conn = null;				
		InputStream in = null; //url.openStream();		
		InputStreamReader inreader = null;
		BufferedReader bufferedreader = null;
		StringBuilder sb = null;							
		int nRead;				
		char[] cdata = new char[16384];
		
		try {
			url = new URL(apiurl);
			conn = (HttpURLConnection)url.openConnection();
			in = conn.getInputStream();														
		}
		catch(Exception e)
		{
			e.printStackTrace();
            e.getMessage();
			in =conn.getErrorStream(); 
		}		
						
		try
		{			
			inreader = new InputStreamReader(in, "UTF-8");
			bufferedreader = new BufferedReader(inreader);  					
			sb = new StringBuilder();

			while((nRead = bufferedreader.read(cdata, 0, cdata.length)) >0)
				sb.append(cdata, 0, nRead);			
		}
		catch(Exception e)
		{			
			e.printStackTrace();
            e.getMessage();
			System.out.println(e.getMessage());			
		}
		finally
		{
			if (in != null)
			{
				try {
					in.close();
				} catch (IOException e) {
					e.getMessage();
				}
			}
			if (inreader != null)
			{
				try {
					inreader.close();
				} catch (IOException e) {
					e.getMessage();
				}
			}
			
			if (bufferedreader != null)
			{
				try {
					bufferedreader.close();
				} catch (IOException e) {					
					e.getMessage();
				}				
			}
		}

        return sb.toString();
    }
    
	private void dataConverter(JsonArray jsonarray)
    {
		for(int i =0; i <jsonarray.size(); i++)
		{
			Gson gson = new Gson();
			PrizeCity prizecity = null;
			prizecity = gson.fromJson(jsonarray.get(i), PrizeCity.class);	
					
			//System.out.println(gson.toJson(prizecity));			
			dataAdaptor(prizecity);
			
		}        
    }

	private void dataAdaptor(PrizeCity prizecity)
	{
		try(DBSQLServer dbs = new DBSQLServer()){
			dbs.addPrizeCity(prizecity);
		}
		catch (Exception e)
		{
			e.getMessage();
		}
	}
}
