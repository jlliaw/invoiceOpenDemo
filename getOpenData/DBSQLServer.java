package my.invoice;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DBSQLServer implements AutoCloseable {
    private Connection _conn;

    public DBSQLServer(String serverName, String databaseName, String userName, String userPassword)    
    {
        _conn = null;        
        String dbURL = "jdbc:sqlserver://%s:1433;databasename=%s;encrypt=false";                        
        dbURL = String.format(dbURL,serverName, databaseName);
        try {
            _conn = DriverManager.getConnection(dbURL, userName, userPassword);
        } catch (SQLException ex) {
            ex.printStackTrace();
            ex.getMessage();
        }            
    }

    public DBSQLServer()
    {
        String dbURL = "jdbc:sqlserver://192.168.56.1:1433;databasename=DBInvoice;encrypt=false";                          
        String user = "invoiceUser";
        String pass = "invoiceUser";
        _conn = null;
        try {
            _conn = DriverManager.getConnection(dbURL, user, pass);
        } catch (SQLException ex) {
            ex.printStackTrace();
            ex.getMessage();
        }            
    }

    @Override
    public void close() throws Exception {
        if (_conn != null && !_conn.isClosed()) _conn.close();        
    }

    public void addPrizeCity(PrizeCity prizecity)
    {
        String isql = "INSERT INTO dbo.PrizeCity"
                    +"(prizeNm, townCd, townNm, invoiceAwardTotalAmt, awardAmt, invoiceAwardTotalCnt, awardDate, yearNm, hsnCd, prize, hsnNm, awardDateNm)"
                    +"VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        
        PreparedStatement stmt = null;        
            
		try 
		{	            
            stmt = _conn.prepareStatement(isql);
            stmt.setString(1, prizecity.getPrizeNm());				
            stmt.setString(2, prizecity.getTownCd());
            stmt.setString(3, prizecity.getTownNm());
            stmt.setInt(4, prizecity.getInvoiceAwardTotalAmt());
            stmt.setInt(5, prizecity.getAwardAmt());
            stmt.setInt(6, prizecity.getInvoiceAwardTotalCnt());

            stmt.setString(7, prizecity.getAwardDate());				
            stmt.setString(8, prizecity.getYearNm());
            stmt.setString(9, prizecity.getHsnCd());

            stmt.setString(10, prizecity.getPrize());				
            stmt.setString(11, prizecity.getHsnNm());
            stmt.setString(12, prizecity.getAwardDateNm());

            stmt.executeUpdate();													

		} catch (SQLException e) {			
			e.getMessage();
		}
		finally
		{			
			if(stmt != null) try{stmt.close();}catch(Throwable e){}			
		}											    
    }
}
