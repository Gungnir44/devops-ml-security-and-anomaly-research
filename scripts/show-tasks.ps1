Get-ScheduledTask -TaskName 'DevOps-*' | ForEach-Object {
    $info = Get-ScheduledTaskInfo -TaskName $_.TaskName
    [PSCustomObject]@{
        TaskName = $_.TaskName
        State = $_.State
        NextRun = $info.NextRunTime
    }
} | Format-Table -AutoSize
