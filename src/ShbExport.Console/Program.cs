using QRCoder;
using ShbExport.Console;

// See https://aka.ms/new-console-template for more information


// var qrGenerator = new AsciiQrGenerator();
// Console.WriteLine(qrGenerator.GenerateAsciiQrCode("Hello World! Hello World! Hello World! Hello World! Hello World! Hello World!"));

var result = BitmapQrReader.ReadQrCode(@"C:\t\qr1.bmp");

Console.WriteLine(result);