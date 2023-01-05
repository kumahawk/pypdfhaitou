from pdfminer.high_level import extract_text
import re
import textwrap
import glob

def remcomma(t):
  return re.sub(',', '', t)

def extractHaitou5(t):
  pat1 = textwrap.dedent('''\
      徴収税額
      
      [ ]*([\d.,]+)(?#1.数量)
      
      [ ]*([\d.,]+)(?#2.配当金等金額)

      [ ]*([\d.,]+)(?#3.外国源泉徴収税額)

      [ ]*([\d.,]+)(?#4.外国手数料)

      [ ]*([\d.,]+)(?#5.外国精算金額)
      外貨
      円貨[ ]*

      [ ]*([\d.,]+)(?#6.国内源泉徴収税額)[ ]*([\d.,]+)(?#7.国内手数料)
      [ ]*

      [ ]*([\d.,]+)(?#8.消費税)

      [ ]*([\d.,]+)(?#9.受取金額)
      [ ]*
      
      [（]国内源泉徴収税の明細[）]
      
      申告レート基準日

      為替レート基準日
      ([\d/]+)
      ([\d/]+)

      申告レート
      為替レート
      [ ]*([\d.]+)
      [ ]*([\d.]+)

      配当金等金額[（]円[）]

      国内課税所得額[（]円[）]

      所得税

      地方税

      外国源泉
      徴収税額[（]円[）]

      国内源泉
      徴収税額

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)

      外貨
      [ ]*([\d.,]+)
      円貨[ ]*([\d.,]+)

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)
      [ ]*([\d.,]+)\
      ''')
  pat2 = textwrap.dedent('''\
      徴収税額
      
      [ ]*([\d.,]+)(?#1.数量)
      
      [ ]*([\d.,]+)(?#2.配当金等金額)

      [ ]*([\d.,]+)(?#3.外国源泉徴収税額)

      [ ]*([\d.,]+)(?#4.外国手数料)

      [ ]*([\d.,]+)(?#5.外国精算金額)
      外貨
      円貨[ ]*

      [ ]*([\d.,]+)(?#6.国内源泉徴収税額)[ ]*([\d.,]+)(?#7.国内手数料)
      [ ]*

      [ ]*([\d.,]+)(?#8.消費税)

      [ ]*([\d.,]+)(?#9.受取金額)
      [ ]*
      
      [（]国内源泉徴収税の明細[）]
      
      申告レート基準日

      為替レート基準日
      ([\d/]+)
      ([\d/]+)

      申告レート
      為替レート
      [ ]*([\d.]+)
      [ ]*([\d.]+)

      配当金等金額[（]円[）]

      国内課税所得額[（]円[）]

      所得税

      地方税

      外国源泉
      徴収税額[（]円[）]

      国内源泉
      徴収税額

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)
      外貨
      円貨[ ]*([\d.,]+)

      [ ]*([\d.,]+)

      [ ]*([\d.,]+)
      [ ]*([\d.,]+)\
      ''')
  m1 = re.search('銘柄コード\n+304-(.+)\n+決済方法', t)
  pat = pat1
  r = []
  while m1:
    nm = str.strip(m1.group(1))
    t = t[m1.end():]
    m2 = re.search(pat, t)
    xx = m2.group(1)
    pat = pat2
    dt1 = remcomma(m2.group(10))
    dt = remcomma(m2.group(11))
    tp = remcomma(m2.group(14))
    ft = remcomma(m2.group(15))
    dp = remcomma(m2.group(16))
    nt = remcomma(m2.group(18))
    lt = remcomma(m2.group(21))
    ftp = remcomma(m2.group(2))
    fft = remcomma(m2.group(3))
    t = t[m2.end():]
    r += [f'"{dt1}","{dt}","{nm}",{tp},{ft},{dp},{nt},{lt},{ftp},{fft}']
    m1 = re.search('銘柄コード\n+304-(.+)\n+決済方法', t)
  return '\n'.join(r)

def extractHaitou6(t):
  pat = textwrap.dedent('''\
    (?P<dt>[\d/]+)(?#1.配当金等支払日)

    (?P<fdt>[\d/]+)(?#2.国内支払日)

    ([\d/]+)(?#3.現地基準日)

    304-(?P<nm>.+)(?#4.銘柄コード)

    (.+)(?#5.銘　柄　名)

    [%]

    1

    ([\d.,-]+)(?#6.外国源泉税率)

    ([\d.,-]+)(?#7.1単位あたり金額)

    ([\d.,-]+)(?#8.数量)

    (?P<ftp>[\d.,-]+)(?#9.配当金等金額)

    (?P<fft>[\d.,-]+)(?#10.外国源泉徴収税額)

    ([\d.,-]+)(?#11.外国手数料)

    ([\d.,-]+)(?#12.外国精算金額)

    ([\d.,-]+)(?#13.国内源泉徴収税額)

    ([\d.,-]+)(?#14.国内手数料)

    ([\d.,-]+)(?#15.消費税)

    ([\d.,-]+)(?#16.受取金額)

    ([\d/]+)(?#17.申告レート基準日)
    ([\d/]+)(?#18.為替レート基準日)

    ([\d.,-]+)(?#19.申告レート)
    ([\d.,-]+)(?#20.為替レート)

    (?P<tp>[\d.,-]+)(?#21.配当金等金額（円）)

    (?P<ft>[\d.,-]+)(?#22.外国源泉徴収税額（円）)

    (?P<dp>[\d.,-]+)(?#23.国内課税所得額（円）)

    ([\d.,-]+)(?#24.所得税外貨)
    (?P<nt>[\d.,-]+)(?#25.所得税円貨)

    ([\d.,-]+)(?#26.地方税外貨)
    (?P<lt>[\d.,-]+)(?#27.地方税円貨)

    ([\d.,-]+)(?#28.国内源泉徴収税額)
    ''')
  t = re.sub('0120-104-214\n+', '', t)
  t = re.sub('gT\n+', '', t)
  r = []
  for m2 in re.finditer(pat, t):
    nm = str.strip(m2.group("nm"))
    dt = remcomma(m2.group("fdt"))
    fdt = remcomma(m2.group("dt"))
    ftp = remcomma(m2.group("ftp"))
    fft = remcomma(m2.group("fft"))
    tp = remcomma(m2.group("tp"))
    ft = remcomma(m2.group("ft"))
    dp = remcomma(m2.group("dp"))
    nt = remcomma(m2.group("nt"))
    lt = remcomma(m2.group("lt"))
    r += [f'"{fdt}","{dt}","{nm}",{tp},{ft},{dp},{nt},{lt},{ftp},{fft}']    
  return '\n'.join(r)

#text = extract_text('G:\\マイドライブ\\令和4年確定申告\\SBI証券\\H20220630.pdf')
#r = extractHaitou6(text)
#print(r)
#exit(0);
for f in glob.glob('G:\\マイドライブ\\令和4年確定申告\\SBI証券\\H2022*.*'):
  m = re.search('H([\d]+)[.](pdf|PDF)$', f)
  if m:
    try:
      fdt = m.group(1)
      text = extract_text(f)
      print(text)
      if fdt < '20210400':
        r = extractHaitou5(text)
      else:
        r = extractHaitou6(text)
      if r == "":
        print("error:"+f)
      else:
        print(r)
    except Exception as e:
      raise e
