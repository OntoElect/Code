using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Data;
using System.Data.OleDb;

namespace ConsoleApplication32
{
    class Program
    {
        static IEnumerable<String> Treatment(String in_txt_dir, //имя каталога, в котором входные ТХТ файлы
                                 String out_dataset_dir, // имя каталога, в который записывать выходные датасеты                  
                                 String strategy, // порядок, в котором выбирать файлы из in_txt_dir                         
                                 int increment_size, // количество файлов, которые добавляются к очередному датасету                        
                                 String citations // имя XLS файла, состоящего из двух колонок: частота цитирования | имя ТХТ файла
                                    )
        {
            List<String> result = null; // список всех возвращаемых адресов
            Array fromDir = null; // массив всех адресов содержащихся в каталоге in_txt_dir
            int length = 0; // будет использоваться при strategy = bi-dir И strategy = random для хранения общего количества файлов находящихся в каталоге in_txt_dir 
            switch (strategy)
            {
                case "chrono": // в хронологическом порялке (более ранние в начале), по данным из имени файла
                    return GetFiles(in_txt_dir)/*получеем массив названий файлов*/.OrderBy(e => e)/*сортируем по возрастанию*/.Take(increment_size)/*возвращаем необходимое количество*/;
                case "rev-chrono": // в порядке, противоположном хронологическому (более поздние в начале)
                    return GetFiles(in_txt_dir)/*получеем массив названий файлов*/.OrderByDescending(e => e)/*сортируем по возрастанию*/.Take(increment_size)/*возвращаем необходимое количество*/;
                case "bi-dir": // попеременно – самый ранний, за ним самый поздний, за ним самый ранний из оставшихся, и т. д.
                    result = new List<String>(); // создаем список который будет содержать список имен возвращаемых файлов
                    fromDir = GetFiles(in_txt_dir).OrderBy(e => e).ToArray<String>(); // получаем массив всех имен файлов в каталоге in_txt_dir
                    length = fromDir.Length - 1; // общее количество файлов находящихся в каталоге in_txt_dir (- 1 т.к. индексация начинается с 0)
                    for (int i = 0; i < increment_size; i++)
                    {

                        if (i % 2 == 0) // добавлем в result берем из начала массива fromDir элемент с индексом i/2
                            result.Add(fromDir.GetValue(i/2) as String);
                        else // добавлем в result берем с конца массива fromDir элемент с индексом 
                            result.Add(fromDir.GetValue(length - ((i - 1)/2)) as String);
                    }
                    return result;

                case "random": // в случайном порядке (если файл уже добавлен, он больше не добавляется)
                    result = new List<String>(); // создаем список который будет содержать список имен возвращаемых файлов
                    List<String> list = GetFiles(in_txt_dir).OrderBy(e => e).ToList<String>(); // получаем список всех имен файлов в каталоге in_txt_dir
                    length = list.Count; // определяем количество имен файлов в каталоге in_txt_dir
                    Random random = new Random(); // определяем объект для генерации случайных чисел
                    while (result.Count < increment_size && list.Count > 0) // выполняем добавление пока количество имен в result меньше increment_size, и list не пуст
                    {
                        int index = random.Next(0, list.Count); // генерим случайное число минимальное значение 0 максмальное количество файлов в list.Count (не включительно)
                        result.Add(list[index]); // добавляем данное имя файла в результирующий набор
                        list.RemoveAt(index); // удаляем его из списка всех файлов что-бы не выбрать повторно
                    }

                    return result;
                case "DCF": // в порядке убывающей частоты цитирования. Данные в XLS файле
                    DataTable dt = Utility.ExcelFile(citations);
                    DataRow row = dt.NewRow();
                    row[0] = dt.Columns[0].Caption;
                    row[1] = dt.Columns[1].Caption.Replace("#",".");
                    dt.Rows.Add(row);
                    return dt.Rows.Cast<DataRow>().OrderBy(e => e[0].ToString()).Select(e => e[1].ToString()).Take(increment_size).ToList();
                default:
                    result = new List<string>(); // возвращаем пустой список
                    break;
            }

            return result;
        }

        // GetFiles
        //----------------------------------------------------------------------------------------------------------------------------------
        /*
         параметры
         * directory - папка в которой содержатся файлы
         * part - расширение (т.к. в данной папке наверное будет содержаться файл Excel определяющий логику конкатенации)
         
         возвращает - список путей содержащихся в папке файлов
         */

        static List<String> GetFiles(String directory, String part = "*.txt") //
        {
            return Directory.GetFiles(directory, "*.txt").ToList<String>();
        }

        // ConcatFiles
        //----------------------------------------------------------------------------------------------------------------------------------
        /*
         параметры
         * filespaths - список строк пути к файлам
         * newname - новое имя файла если пустая строка генерим имя используя текущую дату (чем гарантируем уникальность названий)
         * separator - разделитель который будет вставляться между содержимым разных файлов
         
           возвращает - имя созданного файла 
         */

        static String ConcatFiles(List<String> filespaths, String newname = "", String separator = "")
        {
            if (newname == "") // если пустая строка генерим имя используя текущую дату (чем гарантируем уникальность названий)
                newname = DateTime.Now.ToString("ddMMyyyyhhmmssfff") + ".txt";

            // создаем файл
            /*
             необходимо обсудить что делать если файл существует (перезаписать, добавить новый(тогда необходимо изменить название), выдавать исключение)
             */
            FileInfo finew = new FileInfo(newname);
            StreamWriter finewsr = finew.CreateText();

            byte[] byteArray = Encoding.UTF8.GetBytes(separator);
            MemoryStream mstream = new MemoryStream(byteArray);
            
            foreach (String path in filespaths)
            {
                FileInfo fi = new FileInfo(path);

                StreamReader read = fi.OpenText();
                String line = null;
                while ((line = read.ReadLine()) != null) // записываем построчно
                {
                    finewsr.WriteLine(line); // записываем строку
                }

                if (separator != "") // вставляем сепаратор
                    finewsr.WriteLine(separator);
                
                read.Close();

               
            }
            finewsr.Close();
            
            return newname;
        }





        static void Main(string[] args)
        {

        }
    }

    public static class Utility
    {
        public static object[] ConvertCSVtoDataTable(string strFilePath)
        {
            DataTable dt = new DataTable();
            using (StreamReader sr = new StreamReader(strFilePath))
            {
                string[] headers = sr.ReadLine().Split(',');
                foreach (string header in headers)
                {
                    dt.Columns.Add(header);
                }

                while (!sr.EndOfStream)
                {
                    string[] rows = sr.ReadLine().Split(',');
                    if (rows.Length > 1)
                    {
                        DataRow dr = dt.NewRow();
                        for (int i = 0; i < headers.Length; i++)
                        {
                            dr[i] = rows[i].Trim();
                        }
                        dt.Rows.Add(dr);
                    }
                }
            }


            return new[] { dt, null };
        }

        public static DataTable ExcelFile(String path1)
        {
            DataTable dt = null;

            string extension = System.IO.Path.GetExtension(path1).ToLower();
            string query = null;
            string connString = "";

            string[] validFileTypes = { ".xls", ".xlsx", ".csv" };

            if (validFileTypes.Contains(extension))
            {
                //if (System.IO.File.Exists(path1))
                //{ System.IO.File.Delete(path1); }
                if (extension == ".csv")
                {
                    object[] obj_ = Utility.ConvertCSVtoDataTable(path1);
                    if (obj_[1] == null)
                        dt = obj_[0] as DataTable;

                }
                //Connection String to Excel Workbook  
                else if (extension.Trim() == ".xls")
                {
                    connString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + path1 + ";Extended Properties=\"Excel 8.0;HDR=Yes;IMEX=2\"";
                    object[] obj_ = Utility.ConvertXSLXtoDataTable(path1, connString);
                    if (obj_[1] == null)
                        dt = obj_[0] as DataTable;
                }
                else if (extension.Trim() == ".xlsx")
                {
                    connString = "Provider=Microsoft.ACE.OLEDB.12.0;Data Source=" + path1 + ";Extended Properties=\"Excel 12.0;HDR=Yes;IMEX=2\"";
                    object[] obj_ = Utility.ConvertXSLXtoDataTable(path1, connString);
                    if (obj_[1] == null)
                        dt = obj_[0] as DataTable;
                }
            }

            return dt;
        }

        public static object[] ConvertXSLXtoDataTable(string strFilePath, string connString)
        {
            OleDbConnection oledbConn = new OleDbConnection(connString);
            DataTable dt = new DataTable();
            try
            {
                oledbConn.Open();
                DataTable schemaTable = oledbConn.GetOleDbSchemaTable(OleDbSchemaGuid.Tables, new object[] { null, null, null, "TABLE" });
                using (OleDbCommand cmd = new OleDbCommand(String.Format("SELECT * FROM [{0}]", (string)schemaTable.Rows[0].ItemArray[2]), oledbConn))
                {
                    OleDbDataAdapter oleda = new OleDbDataAdapter();
                    oleda.SelectCommand = cmd;
                    DataSet ds = new DataSet();
                    oleda.Fill(ds);

                    dt = ds.Tables[0];
                }
            }
            catch (Exception ex)
            {
                return new[] { null, ex.Message };
            }
            finally
            {

                oledbConn.Close();
            }

            return new[] { dt, null };

        }
    }
}
