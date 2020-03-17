# getpicture-from-ftp
This software is released under the MIT License, see LICENSE.txt.

FTPサーバの任意ディレクトリ内にある画像ファイル名と，ローカルの任意ディレクトリ内にある画像ファイル名を確認して，FTPサーバにしかない画像ファイルのみをダウンロードするプログラム．

ダウンロードした画像を適当なサイズの円形にトリミングしてから保存している．
円形トリミングの方法の都合上，トリミング後にpng形式で保存する必要がある．  
FTPサーバにあるjpgファイルをダウンロードしてトリミングしてpngで保存する．

顔アイコン画像取得のために，launchd(https://qiita.com/rsahara/items/7d37a4cb6c73329d4683)で定期的に自動実行されるようにして使った．

aftertasteの「picture_name.csv」は，このプログラムで生成・上書きされるファイルである．合わせて見てもらうと，感じを掴みやすいかも．．．