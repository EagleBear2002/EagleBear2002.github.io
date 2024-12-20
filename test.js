var levelCount = [0, 0, 0, 0, 0, 0, 0]; // 用于记录各级标题的计数

function PrintBookmarks(bm, nLevel) {
    if (nLevel != 0) { // don't print the root
        bmReport.absIndent = bmTab * (nLevel - 1);
        bm.execute();

        // 添加层级序号，从二级标题开始编号
        var title = getNumberedTitle(bm.name, nLevel);

        var pageNum = (bm.doc.pageNum + 1).toString();

        // 计算标题和页码的字符长度，包括中文字符
        var titleLen = countCharacters(title);
        var pageNumLen = countCharacters(pageNum);

        // var rptnum = Math.floor((totalWidth - titleWidth - pageNumWidth) / measureTextWidth('.'));
        var dots = '.'.repeat(50 - titleLen - pageNumLen); // 总宽度为50，减去标题长度和页码长度，计算出点号的个数
        bmReport.writeText(title + dots + pageNum, { align: "right" });
        // bmReport.vspace(12); // 增大行间距
    }
    if (bm.children != null)
        for (var i = 0; i < bm.children.length; i++)
            PrintBookmarks(bm.children[i], nLevel + 1);
}

// 获取层级序号，从二级标题开始编号
function getNumberedTitle(title, nLevel) {
    if (nLevel === 1) {
        return title;
    }

    levelCount[nLevel]++; // 当前层级计数增加

    // 生成层级序号
    var numberedTitle = "";
    for (var i = 2; i <= nLevel; i++) {
        numberedTitle += levelCount[i] + ".";
    }

    // 添加标题内容
    numberedTitle += " " + title;
    return numberedTitle;
}

// 计算字符长度，包括中文字符
function countCharacters(str) {
    var count = 0;
    for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) > 127) {
            count += 2; // 中文字符占两个字符长度
        } else {
            count += 1;
        }
    }
    return count;
}

bmTab = 15; // 调整缩进的距离，使目录更美观
bmReport = new Report();
bmReport.size = 2;
bmReport.writeText(this.title);
bmReport.writeText(" ");
bmReport.size = 1.5;
bmReport.writeText("目录");
bmReport.writeText(" ");
bmReport.size = 1;
PrintBookmarks(this.bookmarkRoot, 0);
global.bmRep = bmReport; // make global

// 使用try-catch块确保目录页的生成不会出错
global.wrtDoc = app.setInterval(
    'try {' +
    ' reportDoc = global.bmRep.open("Listing of Bookmarks");' +
    ' console.println("Executed Report.open");' +
    ' app.clearInterval(global.wrtDoc);' +
    ' delete global.wrtDoc;' +
    ' console.println("Executed App.clearInterval");' +
    ' reportDoc.info.title = "Bookmark Listings";' +
    ' reportDoc.info.Author = "List Bookmark Sequence";' +
    '} catch (e) {console.println("Waiting...: " + e);}', 100);