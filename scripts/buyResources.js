$.ajax({
    type: "POST",
    dataType: "json",
    url: "/ajax.php?mod=suppliers&tab=empty&atype=json",
    encoding:"UTF-8",
    data: "<data>&action=save-buy-decision-value",
    error: () => {
        setTimeout(function() {
            self.location = `${root_path}/logout.php`
        }, 1000);
    }
});
