# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 08:47:35 2019

@author: abran
"""

$("#myClickButton").click(function() {
    $.get("/output/", function(data) {
        $("#myOutput").html(data);
    }, "html");
});